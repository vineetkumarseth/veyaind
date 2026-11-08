"""Build the training set for Veya Code Tutor.

  python make_dataset.py seed                       # write data/seed.jsonl (10 gold examples)
  python make_dataset.py generate --count 300       # ask your local teacher model (Ollama) to write more, keep only valid ones
  python make_dataset.py build                      # validate, remove duplicates, split into data/train.jsonl and data/val.jsonl
  python make_dataset.py review --n 8               # print random examples. READ THEM. Delete bad ones from data/raw.jsonl.

Only the standard library is used."""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from data_utils import load_jsonl  # noqa: E402
from seeds import SEEDS, as_messages  # noqa: E402
from topics import TOPICS  # noqa: E402
from tutor_prompt import TUTOR_SYSTEM  # noqa: E402
from validate import validate  # noqa: E402

DATA = os.path.join(HERE, "data")
Q = {"en": ["Explain {t} to a complete beginner.", "I am new to programming. What is {t}?", "Teach me {t} with a simple example."],
     "hinglish": ["{t} kya hota hai? Beginner ke liye simple me samjhao.", "{t} samjhao, bilkul basic se.", "Mujhe {t} sikhao, example ke saath."]}


def on_topic(topic: str, answer: str) -> bool:
    """Cheap check that the answer really talks about the topic (small models sometimes drift)."""
    words = [w for w in re.findall(r"[a-z_]{4,}", topic.lower()) if w not in {"with", "and", "the", "for", "basics", "common"}]
    low = answer.lower()
    return not words or any(w[:5] in low for w in words)


def ollama_chat(model: str, messages: list, host: str = "http://localhost:11434", temperature: float = 0.6) -> str:
    body = {"model": model, "messages": messages, "stream": False, "options": {"temperature": temperature, "num_ctx": 8192, "num_predict": 1500}}
    if model.startswith("qwen3"):
        body["think"] = False
    req = urllib.request.Request(host + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["message"]["content"].strip()


def cmd_seed(_):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "seed.jsonl"), "w", encoding="utf-8") as f:
        for s in SEEDS:
            f.write(json.dumps(as_messages(s), ensure_ascii=False) + "\n")
    print(f"wrote {len(SEEDS)} gold examples")


def cmd_generate(a):
    raw = os.path.join(DATA, "raw.jsonl")
    os.makedirs(DATA, exist_ok=True)
    done = {(r["topic"], r["lang"]) for r in load_jsonl(raw)} if os.path.exists(raw) else set()
    combos = [(t, l) for t in TOPICS for l in (["en", "hinglish"] if a.lang == "both" else [a.lang]) if (t, l) not in done]
    random.Random(a.seed).shuffle(combos)
    ok = rej = 0
    for t, lang in combos[: a.count]:
        shots = [s for s in SEEDS if s["lang"] == lang and s["topic"] != t][:2]
        msgs = [{"role": "system", "content": TUTOR_SYSTEM}]
        for s in shots:  # two gold examples show the exact style
            msgs += [{"role": "user", "content": s["q"]}, {"role": "assistant", "content": s["a"]}]
        q = random.Random(f"{t}{lang}").choice(Q[lang]).format(t=t)
        msgs.append({"role": "user", "content": q})
        try:
            ans = ollama_chat(a.model, msgs, a.host)
        except Exception as e:  # Ollama off, model missing, timeout
            print("stopped:", e)
            break
        problems = validate(ans, lang) or ([] if on_topic(t, ans) else ["answer is not about the topic"])
        if problems:
            rej += 1
            print(f"  rejected [{t} / {lang}]: {problems[0]}")
            continue
        with open(raw, "a", encoding="utf-8") as f:
            f.write(json.dumps({"topic": t, "lang": lang, "messages": [msgs[0], {"role": "user", "content": q}, {"role": "assistant", "content": ans}]}, ensure_ascii=False) + "\n")
        ok += 1
        print(f"  kept     [{t} / {lang}]  ({ok} kept, {rej} rejected)")
    print(f"done: {ok} kept, {rej} rejected. Next: python make_dataset.py review")


def cmd_build(a):
    rows, seen, dropped = [], set(), 0
    for r in (load_jsonl(os.path.join(DATA, "raw.jsonl")) if os.path.exists(os.path.join(DATA, "raw.jsonl")) else []):
        ans = r["messages"][-1]["content"]
        h = hashlib.md5(ans.encode()).hexdigest()
        if validate(ans, r["lang"]) or not on_topic(r["topic"], ans) or h in seen:
            dropped += 1
            continue
        seen.add(h)
        rows.append(r)
    random.Random(7).shuffle(rows)
    gold = [as_messages(s) for s in SEEDS]
    if len(rows) >= 10:
        k = max(2, len(rows) // 10)
        val, train = rows[:k], rows[k:] + gold * 2  # gold examples count double
    else:  # not enough generated data yet: train on gold only, so the pipeline can still be tested
        val, train = gold[:2], gold
    for name, part in (("train", train), ("val", val)):
        with open(os.path.join(DATA, f"{name}.jsonl"), "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps({"messages": r["messages"]}, ensure_ascii=False) + "\n")
    print(f"train {len(train)} | val {len(val)} | dropped {dropped}. Aim for 300+ train rows before you fine-tune.")


def cmd_review(a):
    rows = load_jsonl(os.path.join(DATA, "raw.jsonl"))
    for r in random.sample(rows, min(a.n, len(rows))):
        print("=" * 70, f"\n[{r['topic']} / {r['lang']}]\nQ: {r['messages'][1]['content']}\n\n{r['messages'][2]['content']}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed").set_defaults(f=cmd_seed)
    g = sub.add_parser("generate")
    g.add_argument("--model", default="qwen3:8b")
    g.add_argument("--count", type=int, default=300)
    g.add_argument("--lang", choices=["en", "hinglish", "both"], default="both")
    g.add_argument("--host", default="http://localhost:11434")
    g.add_argument("--seed", type=int, default=1)
    g.set_defaults(f=cmd_generate)
    sub.add_parser("build").set_defaults(f=cmd_build)
    r = sub.add_parser("review")
    r.add_argument("--n", type=int, default=8)
    r.set_defaults(f=cmd_review)
    a = ap.parse_args()
    a.f(a)
