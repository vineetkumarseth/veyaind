"""Score a model on 12 tutor questions it has never seen. Run it for the baseline AND for your tuned model:

  python eval_tutor.py --model qwen3:8b          # baseline: big model + the tutor prompt
  python eval_tutor.py --model veya-tutor        # your fine-tuned model
Ship the tuned model only if it scores clearly better, or is almost as good but much smaller/faster."""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from make_dataset import ollama_chat  # noqa: E402
from tutor_prompt import TUTOR_SYSTEM  # noqa: E402
from validate import validate  # noqa: E402

TESTS = [("hinglish", "while loop kya hota hai? Samjhao."), ("en", "What is a stack? Explain with an example."), ("hinglish", "String slicing samjhao."),
         ("en", "What is a linked list?"), ("hinglish", "Class aur object kya hote hain?"), ("en", "Explain SQL JOIN to a beginner."),
         ("hinglish", "Selection sort samjhao."), ("en", "What is a queue?"), ("hinglish", "try-except kya hota hai?"),
         ("en", "Explain Git commit and branch."), ("hinglish", "List comprehension samjhao."), ("en", "What is time complexity?")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--host", default="http://localhost:11434")
    a = ap.parse_args()
    passed, lines = 0, [f"# Tutor eval: {a.model}\n"]
    for lang, q in TESTS:
        t0 = time.time()
        try:
            ans = ollama_chat(a.model, [{"role": "system", "content": TUTOR_SYSTEM}, {"role": "user", "content": q}], a.host)
        except Exception as e:
            sys.exit(f"Could not reach the model: {e}")
        bad = validate(ans, lang)
        passed += not bad
        print(f"{'PASS' if not bad else 'FAIL'}  {q}  ({time.time() - t0:.0f}s)" + (f"  -> {bad[0]}" if bad else ""))
        lines.append(f"## {q}\nformat check: {'PASS' if not bad else 'FAIL: ' + '; '.join(bad)}\n\n{ans}\n")
    print(f"\nformat score: {passed}/{len(TESTS)}  (this checks structure and code syntax, NOT teaching quality: also read the file below)")
    out = f"eval_{a.model.replace(':', '_').replace('/', '_')}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Read the answers in", out)


if __name__ == "__main__":
    main()
