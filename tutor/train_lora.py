"""Fine-tune a small open model into Veya Code Tutor with LoRA, in plain PyTorch (no trainer framework).

Easiest place to run: a free Google Colab or Kaggle GPU.  On a Mac it works only as a tiny smoke test (--smoke).

  pip install -r requirements-train.txt
  python train_lora.py --smoke                  # 3 quick steps, checks that everything is installed
  python train_lora.py --epochs 3               # real run, uses data/train.jsonl and data/val.jsonl

Base model: Qwen/Qwen2.5-Coder-1.5B-Instruct (Apache-2.0 licence, checked on its Hugging Face page)."""
import argparse
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_utils import build_example, load_jsonl, lr_at  # noqa: E402

TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-Coder-1.5B-Instruct")
    ap.add_argument("--train", default="data/train.jsonl")
    ap.add_argument("--val", default="data/val.jsonl")
    ap.add_argument("--out", default="out/veya-tutor-lora")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--accum", type=int, default=8, help="examples per optimizer step")
    ap.add_argument("--max_len", type=int, default=2048)
    ap.add_argument("--r", type=int, default=16, help="LoRA rank")
    ap.add_argument("--smoke", action="store_true", help="3 optimizer steps on 4 examples, just to test the setup")
    a = ap.parse_args()

    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float32
    if dev == "cuda":
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16  # Colab T4 has no bf16
    print(f"device={dev} dtype={dtype}")
    if dev != "cuda" and not a.smoke:
        print("WARNING: no NVIDIA GPU found. A real run will be very slow. Use Colab/Kaggle, or add --smoke to test only.")

    tok = AutoTokenizer.from_pretrained(a.base)
    try:
        model = AutoModelForCausalLM.from_pretrained(a.base, dtype=dtype)
    except TypeError:  # older transformers
        model = AutoModelForCausalLM.from_pretrained(a.base, torch_dtype=dtype)
    model.config.use_cache = False
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(r=a.r, lora_alpha=2 * a.r, lora_dropout=0.05, target_modules=TARGETS, task_type="CAUSAL_LM"))
    for p in model.parameters():
        if p.requires_grad:
            p.data = p.data.float()  # keep the small LoRA weights in fp32 for stable training
    model.to(dev)
    model.print_trainable_parameters()

    def prep(path, limit=None):
        rows = load_jsonl(path)[:limit]
        ex = [build_example(r["messages"], tok, a.max_len) for r in rows]
        kept = [e for e in ex if e]
        print(f"{path}: {len(kept)} usable, {len(ex) - len(kept)} skipped (longer than {a.max_len} tokens)")
        return kept

    train, val = prep(a.train, 4 if a.smoke else None), prep(a.val, 2 if a.smoke else None)
    if not train:
        sys.exit("No training examples. Run: python make_dataset.py build")
    steps_per_epoch = max(1, -(-len(train) // a.accum))
    total = 3 if a.smoke else steps_per_epoch * a.epochs
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.0)
    scaler = torch.amp.GradScaler("cuda", enabled=(dev == "cuda" and dtype == torch.float16))
    ctx = lambda: torch.autocast(device_type="cuda", dtype=dtype, enabled=(dev == "cuda"))  # noqa: E731

    def batch(e):
        return torch.tensor([e["input_ids"]], device=dev), torch.tensor([e["labels"]], device=dev)

    def val_loss():
        if not val:
            return float("nan")
        model.eval()
        tot = 0.0
        with torch.no_grad(), ctx():
            for e in val:
                i, l = batch(e)
                tot += model(input_ids=i, labels=l).loss.item()
        model.train()
        return tot / len(val)

    step, t0 = 0, time.time()
    model.train()
    for ep in range(a.epochs):
        random.Random(ep).shuffle(train)
        run = 0.0
        for k, e in enumerate(train):
            i, l = batch(e)
            with ctx():
                loss = model(input_ids=i, labels=l).loss / a.accum
            scaler.scale(loss).backward()
            run += loss.item()
            if (k + 1) % a.accum == 0 or k + 1 == len(train):
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
                for g in opt.param_groups:
                    g["lr"] = lr_at(step, total, max(1, total // 20), a.lr)
                scaler.step(opt)
                scaler.update()
                opt.zero_grad(set_to_none=True)
                step += 1
                if step % 5 == 0 or a.smoke:
                    print(f"epoch {ep + 1} step {step}/{total} loss {run:.4f} ({time.time() - t0:.0f}s)")
                run = 0.0
                if a.smoke and step >= 3:
                    break
        print(f"== epoch {ep + 1} done | validation loss {val_loss():.4f}")
        os.makedirs(a.out, exist_ok=True)
        model.save_pretrained(a.out)
        tok.save_pretrained(a.out)
        if a.smoke:
            break
    print(f"Saved LoRA adapter to {a.out}. Next: python merge_export.py")


if __name__ == "__main__":
    main()
