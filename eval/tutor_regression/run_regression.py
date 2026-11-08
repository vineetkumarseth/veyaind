"""Veya Code Tutor regression suite: 55 fixed cases, six quality dimensions, one record per release.

  python run_regression.py --selftest                       # offline: proves the checkers themselves work (no model needed)
  python run_regression.py --model qwen3:8b --release r1    # online: needs Ollama; writes eval/tutor_regression/releases.jsonl
  python run_regression.py --model veya-tutor --release r2 --run-code   # also RUNS the model's Python (see warning)

Dimensions: technical_accuracy, execution_correctness, visual_correctness, teaching_quality, adaptive_behavior, privacy_context.
Automatic checks are a floor, not a verdict on teaching quality: read the saved answers and fill in human_review."""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tutor"))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from cases import CASES  # noqa: E402
from tutor_prompt import TUTOR_SYSTEM  # noqa: E402
from validate import FENCE, check_visual, validate  # noqa: E402

DIMENSIONS = ["technical_accuracy", "execution_correctness", "visual_correctness", "teaching_quality", "adaptive_behavior", "privacy_context"]
DEVANAGARI = re.compile(r"[\u0900-\u097F]")


def python_blocks(answer):
    return [b for l, b in FENCE.findall(answer) if l.lower() in ("python", "py")]


def run_python(code, timeout=5):
    """Runs model-written code in a temp folder with a time limit. NOT a security sandbox."""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "main.py")
        open(p, "w", encoding="utf-8").write(code)
        try:
            r = subprocess.run([sys.executable, "-I", p], cwd=d, capture_output=True, text=True, timeout=timeout, env={"PATH": "/usr/bin:/bin"})
            return r.returncode == 0, (r.stdout + r.stderr)[-300:]
        except subprocess.TimeoutExpired:
            return False, "timeout"


def evaluate(case, answer, run_code=False):
    """Returns a list of (dimension, check name, passed, detail)."""
    out = []
    flags = re.I
    privacy = case["id"].startswith("pv")
    for rx in case.get("require", []):
        out.append(("technical_accuracy", f"require {rx}", bool(re.search(rx, answer, flags | re.S)), ""))
    for group in case.get("require_any", []):
        out.append(("technical_accuracy", f"any of {group}", any(re.search(rx, answer, flags | re.S) for rx in group), ""))
    for rx in case.get("forbid", []):
        hit = re.search(rx, answer, flags | re.M)
        out.append(("privacy_context" if privacy else "technical_accuracy", f"forbid {rx}", not hit, hit.group(0) if hit else ""))
    if case.get("code"):
        blocks = python_blocks(answer)
        ok, detail = bool(blocks), "no python block"
        for b in blocks:
            try:
                compile(b, "<answer>", "exec")
            except SyntaxError as e:
                ok, detail = False, f"line {e.lineno}: {e.msg}"
                break
            if run_code:
                ran, info = run_python(b)
                if not ran:
                    ok, detail = False, "ran and failed: " + info.strip().splitlines()[-1:][0] if info.strip() else "ran and failed"
                    break
        out.append(("execution_correctness", "python code " + ("ran" if run_code else "compiles"), ok, detail if not ok else ""))
    if case.get("sim"):
        found = None
        for l, b in FENCE.findall(answer):
            if l.lower() == "sim":
                try:
                    o = json.loads(b)
                except ValueError:
                    continue
                if o.get("algo") == case["sim"]:
                    found = (b, o)
        ok = found is not None and check_visual("sim", found[0]) is None
        if ok and case["sim"] == "binary_search" and found[1]["target"] not in found[1]["input"]:
            ok = False  # a demo of a successful search should search for something that is there
        out.append(("visual_correctness", f"valid sim: {case['sim']}", ok, ""))
    if case.get("visual") in ("complexity", "flow"):
        blocks = [(l.lower(), b) for l, b in FENCE.findall(answer) if l.lower() == case["visual"]]
        out.append(("visual_correctness", f"valid {case['visual']} block", bool(blocks) and all(check_visual(l, b) is None for l, b in blocks), ""))
    if case.get("visual") == "table":
        out.append(("visual_correctness", "markdown table", bool(re.search(r"^\|.*\|\s*\n\|[\s:|-]+\|", answer, re.M)), ""))
    if case.get("max_questions") is not None:
        n = answer.count("?")
        out.append(("adaptive_behavior", f"at most {case['max_questions']} question", 1 <= n <= case["max_questions"] if "require" in case and any("?" in r for r in case["require"]) else n <= case["max_questions"], f"{n} question marks"))
    if case.get("adaptive") or case["category"] == "Adaptive tutoring":
        pass
    if case.get("no_devanagari") or case["lang"] == "hinglish":
        out.append(("teaching_quality", "Roman script only", not DEVANAGARI.search(answer), ""))
    if case.get("format", True):
        problems = validate(answer, case["lang"])
        out.append(("teaching_quality", "six-part format, pictures and code are valid", not problems, "; ".join(problems[:2])))
    if case["category"] == "Adaptive tutoring":  # re-label: these checks measure adaptive behaviour
        out = [("adaptive_behavior", n, p, d) if dim in ("technical_accuracy",) else (dim, n, p, d) for dim, n, p, d in out]
    return out


def build_messages(case):
    system = TUTOR_SYSTEM + ("\n" + case["plant"] if case.get("plant") else "")
    msgs = [{"role": "system", "content": system}]
    for role, text in case.get("history", []):
        msgs.append({"role": role, "content": text})
    msgs.append({"role": "user", "content": case["prompt"]})
    return msgs


# ---------- offline self-test: canned good and bad answers prove the checkers catch what they should ----------
def six(idea="Idea text.", visual="| a | b |\n|---|---|\n| 1 | 2 |", code="```python\nprint(1)\n```", steps="1. It prints.", mistake="A mistake.", tryit="Try it yourself."):
    return f"**Idea**\n{idea} " + "x" * 400 + f"\n\n**Visual**\n{visual}\n\n**Code**\n{code}\n\n**Step by step**\n{steps}\n\n**Common mistake**\n{mistake}\n\n**Try it**\n{tryit}"


SIM_BUBBLE = '```sim\n{"algo": "bubble_sort", "input": [5, 2, 9, 1]}\n```'
SELFTEST = {
    "nn01": (six(idea="XOR is not linearly separable, so one straight line cannot split it. A single perceptron fails; add a hidden layer."), six(idea="A single perceptron can learn XOR easily with enough epochs.")),
    "tf02": (six(idea="GPT is decoder-only. The original Transformer is encoder-decoder."), six(idea="GPT is an encoder-decoder model like the original Transformer.")),
    "rc01": (six(visual='```sim\n{"algo": "factorial", "n": 3}\n```', code="```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n```"),
             six(visual='```sim\n{"algo": "factorial", "n": 3}\n```', code="```python\ndef factorial(n):\n    if n == 1\n        return 1\n    return n * factorial(n - 1)\n```")),
    "so01": (six(visual=SIM_BUBBLE, code="```python\nprint(sorted([5, 2, 9, 1]))\n```", steps="1. Press play."), six(visual=SIM_BUBBLE, code="```python\nprint(sorted([5, 2, 9, 1]))\n```", steps="1. After pass one the list is [2, 5, 1, 9].")),
    "so04": (six(visual='```sim\n{"algo": "binary_search", "input": [2, 5, 8], "target": 5}\n```'), six(visual='```sim\n{"algo": "binary_search", "input": [8, 2, 5], "target": 5}\n```')),
    "vz01": (six(visual='```complexity\n{"n": 16, "curves": ["1", "n", "n^2"]}\n```'), six(visual='```chart\n{"type": "bar", "x": ["a"], "y": [1]}\n```')),
    "ad01": ("Let's start. What does `for i in range(2): print(i)` print?", "What prints? Answer: 0 1. Next question: why?"),
    "ad02": ("Close! Notice that range(3) starts at 0, so the output is 0, 1, 2. Does that make sense?", "Correct! It prints 1 2 3."),
    "ad03": ("Theek hai. Ek `for` loop question: `for i in range(3): print(i)` kya print karta hai?", "यह एक सवाल है: loop kya hai? aur for kya hai?"),
    "pv01": (six(visual=SIM_BUBBLE, code="```python\nprint(1)\n```", steps="1. Press play."), six(visual=SIM_BUBBLE, code="```python\nprint(1)\n```", steps="1. Press play.", idea="Vineet from Kanpur, here is bubble sort.")),
    "pv02": (six(idea="Recursion means a function calls itself."), six(idea="Since you are weak at recursion, let us go slowly.")),
    "pv03": ("I don't know anything about you yet.", "You are a B.Tech student and your name is Vineet."),
    "sq02": (six(visual="| id | name |\n|---|---|\n| 1 | A |", idea="INNER JOIN combines rows using ON.", code="```sql\nSELECT * FROM a JOIN b ON a.id = b.id;\n```"), six(visual="no table here", idea="INNER JOIN combines rows using ON.")),
}


def selftest():
    byid = {c["id"]: c for c in CASES}
    bad_count = 0
    for cid, (good, bad) in SELFTEST.items():
        c = byid[cid]
        g = [r for r in evaluate(c, good) if not r[2]]
        b = [r for r in evaluate(c, bad) if not r[2]]
        ok = not g and bool(b)
        bad_count += (not ok)
        print(("PASS " if ok else "FAIL ") + f"{cid}: good answer passes all checks={not g}; bad answer is caught={bool(b)}" + (f"  (good failed: {g[:2]})" if g else ""))
    print(f"selftest: {len(SELFTEST) - bad_count}/{len(SELFTEST)} checker scenarios behave correctly")
    return bad_count == 0


def run(model, host, release, run_code):
    from make_dataset import ollama_chat
    per = {d: [0, 0] for d in DIMENSIONS}
    failed, lines = [], [f"# Tutor regression: {model} ({release})\n"]
    for c in CASES:
        try:
            ans = ollama_chat(model, build_messages(c), host, temperature=0)
        except Exception as e:
            sys.exit(f"Could not reach the model: {e}")
        res = evaluate(c, ans, run_code)
        for dim, name, ok, detail in res:
            per[dim][1] += 1
            per[dim][0] += ok
        bad = [r for r in res if not r[2]]
        if bad:
            failed.append(c["id"])
        print(f"{'PASS' if not bad else 'FAIL'}  {c['id']:5s} {c['category']:24s} " + ("" if not bad else f"-> {bad[0][1]} {bad[0][3]}"))
        lines.append(f"## {c['id']} {c['category']}\nQ: {c['prompt']}\nchecks failed: {[(r[0], r[1], r[3]) for r in bad] or 'none'}\n\n{ans}\n")
    total = sum(v[1] for v in per.values())
    passed = sum(v[0] for v in per.values())
    rec = {"release": release, "date": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "model": model, "execution": "ran" if run_code else "compiled only",
           "cases": len(CASES), "cases_failed": failed, "dimensions": {d: f"{v[0]}/{v[1]}" for d, v in per.items()}, "checks_passed": f"{passed}/{total}",
           "human_review": {"teaching_quality_1_to_5": None, "adaptive_behavior_1_to_5": None, "notes": ""}}
    with open(os.path.join(HERE, "releases.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    out = os.path.join(HERE, "runs", f"{release}_{model.replace(':', '_').replace('/', '_')}.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print("\n" + json.dumps(rec["dimensions"], indent=1) + f"\nchecks passed {rec['checks_passed']}; failed cases: {len(failed)}\nrecorded in releases.jsonl; answers saved to {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--release", default="dev")
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--run-code", action="store_true", help="RUN the model's Python on this computer (not a security sandbox)")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if not a.model:
        ap.error("give --model (or use --selftest)")
    run(a.model, a.host, a.release, a.run_code)
