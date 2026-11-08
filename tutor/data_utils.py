"""Small helpers with no heavy imports, so they can be tested anywhere (no torch needed)."""
import json
import math


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build_example(messages, tok, max_len):
    """Turn [system, user, assistant] into input_ids + labels. Only the assistant part is trained (prompt = -100).
    Returns None when the example is longer than max_len (we skip it instead of cutting code in half)."""
    full = tok.apply_chat_template(messages, tokenize=False)
    prompt = tok.apply_chat_template(messages[:-1], tokenize=False, add_generation_prompt=True)
    if not full.startswith(prompt):
        raise ValueError("chat template does not extend the prompt; check the tokenizer template")
    p_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    f_ids = tok(full, add_special_tokens=False)["input_ids"]
    if f_ids[:len(p_ids)] != p_ids or len(f_ids) > max_len:
        return None
    return {"input_ids": f_ids, "labels": [-100] * len(p_ids) + f_ids[len(p_ids):]}


def lr_at(step, total, warmup, base):
    """Linear warm-up, then cosine decay to 10 percent of base."""
    if step < warmup:
        return base * (step + 1) / max(1, warmup)
    t = (step - warmup) / max(1, total - warmup)
    return base * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, t))))
