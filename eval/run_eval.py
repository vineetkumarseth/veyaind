"""Veya eval: models ko 50 Hinglish sawalon par chalao aur compare karo (sirf Python + Ollama chahiye).

1) python run_eval.py run llama3.1:8b qwen2.5:7b      -> results_<date_time>.csv banta hai (purani file overwrite nahi hoti)
2) results.csv mein khali 'score' column bharo: 0 = galat, 1 = theek-thaak, 2 = achha
   (memory aur kuch maths ke sawalon ka score apne aap bhar jata hai, bas ek nazar daal lo)
3) python run_eval.py score results.csv                -> model-wise comparison
"""
import csv, json, os, re, sys, time, urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from hints import style_hint  # main.py wala hi hint
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
QUESTIONS = json.load(open(os.path.join(HERE, "questions.json"), encoding="utf-8"))
# main.py ke prompts ki copy; main.py badlo to yahan bhi badlo
SYSTEM = ("You are Veya, a helpful and private personal AI. Reply in the user's language and script: Roman Hinglish "
          "(Latin letters) gets Roman Hinglish, never Devanagari; Hindi in Devanagari gets Hindi; English gets English. "
          "Use simple, natural words, keep technical terms in English, and never invent words. "
          "You have no live data (weather, news, prices, scores): say so instead of guessing. "
          "For medical questions give only general safety information and advise seeing a doctor; do not recommend "
          "specific medicines. Be concise and honest; say so when you are unsure."
          " Never state live numbers (prices, rates, scores, news) and never write lines like 'Data: X (just fetched)' unless this system message itself contains live data; never invent sources.")
EXTRACT = ('Extract lasting facts the user explicitly states about THEMSELVES. Rules: never facts about the '
           'assistant; if the user addresses the assistant by name (like "Veya"), that is the assistant\'s name, '
           'not the user\'s; questions and requests contain no facts; never write negative or "not provided" '
           'statements. Write each fact as a short English sentence starting with "The user". '
           'Reply ONLY JSON: {"facts": ["..."]}. Use {"facts": []} if there is nothing.')
BAD = re.compile(r"(?:\bnot|n't)\s+(?:provide|state|mention|specify|share)\w*|\bno (?:facts|information)\b|"
                      r"language model|artificial intelligence|as an ai", re.I)


def call(model, messages, fmt=None):
    body = {"model": model, "stream": False, "messages": messages}
    if fmt:
        body["format"] = fmt
    if model.startswith("qwen3") and os.getenv("VEYA_THINK", "1") == "0":
        body["think"] = False
    req = urllib.request.Request(OLLAMA + "/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.load(r)["message"]["content"].strip()
    return out, time.time() - t


def auto_score(q, answer):
    if q["cat"] == "memory":
        try:
            facts = [f for f in json.loads(answer).get("facts", []) if isinstance(f, str)]
        except Exception:
            return 0
        good = [f for f in facts if f.startswith("The user") and not BAD.search(f) and "veya" not in f.lower()]
        if q.get("empty"):
            return 2 if not good else 0
        text = " ".join(good).lower()
        hits = sum(any(a in text for a in k.split("|")) for k in q["expect"])
    elif q.get("expect"):
        hits = sum(any(a in answer for a in k.split("|")) for k in q["expect"])
    else:
        return ""
    return 2 if hits == len(q["expect"]) else (1 if hits else 0)


def run(models):
    rows = []
    for m in models:
        print(f"\n== {m} ==  (pehle model load ho raha hai)")
        call(m, [{"role": "user", "content": "hi"}])
        for q in QUESTIONS:
            mem = q["cat"] == "memory"
            hs, hu = ("", "") if mem else style_hint(q["q"])
            msgs = [{"role": "system", "content": EXTRACT if mem else SYSTEM + hs}, {"role": "user", "content": q["q"] + hu}]
            try:
                ans, sec = call(m, msgs, "json" if mem else None)
            except Exception as e:
                ans, sec = f"ERROR: {e}", 0
            rows.append({"id": q["id"], "category": q["cat"], "question": q["q"], "model": m, "seconds": round(sec, 1),
                         "answer": ans, "score": auto_score(q, ans)})
            print(f"  {q['id']:>2}/50  {sec:5.1f}s", end="\r")
    out_path = time.strftime("results_%Y%m%d_%H%M.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["id", "category", "question", "model", "seconds", "answer", "score"])
        w.writeheader(); w.writerows(rows)
    print(f"\n{out_path} ban gayi. Khali 'score' bharo (0/1/2), phir: python3 run_eval.py score {out_path}")


def score(path):
    by, secs, missing = defaultdict(lambda: defaultdict(list)), defaultdict(list), 0
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        secs[r["model"]].append(float(r["seconds"] or 0))
        if str(r["score"]).strip() == "":
            missing += 1; continue
        by[r["model"]][r["category"]].append(int(r["score"]))
    cats = sorted({c for m in by.values() for c in m})
    print(f"{'model':<22}{'overall':>8}" + "".join(f"{c[:9]:>11}" for c in cats) + f"{'sec/ans':>9}")
    for m, d in by.items():
        allv = [s for v in d.values() for s in v]
        pct = lambda v: f"{100 * sum(v) / (2 * len(v)):.0f}%" if v else "-"
        print(f"{m:<22}{pct(allv):>8}" + "".join(f"{pct(d.get(c, [])):>11}" for c in cats) + f"{sum(secs[m]) / len(secs[m]):>9.1f}")
    if missing:
        print(f"\n{missing} jawab abhi unscored hain, unko bharo to comparison poora hoga.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "run":
        run(a[1:])
    elif len(a) == 2 and a[0] == "score":
        score(a[1])
    else:
        print(__doc__)
