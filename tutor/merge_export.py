"""Merge the LoRA adapter into the base model and save a normal Hugging Face model folder (out/merged).
Then convert it to GGUF for Ollama with export_gguf.sh."""
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-Coder-1.5B-Instruct")
    ap.add_argument("--adapter", default="out/veya-tutor-lora")
    ap.add_argument("--out", default="out/merged")
    a = ap.parse_args()
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    try:
        base = AutoModelForCausalLM.from_pretrained(a.base, dtype=torch.float16)
    except TypeError:
        base = AutoModelForCausalLM.from_pretrained(a.base, torch_dtype=torch.float16)
    merged = PeftModel.from_pretrained(base, a.adapter).merge_and_unload()
    merged.save_pretrained(a.out, safe_serialization=True)
    AutoTokenizer.from_pretrained(a.base).save_pretrained(a.out)
    print(f"Merged model saved to {a.out}. Next: bash export_gguf.sh")


if __name__ == "__main__":
    main()
