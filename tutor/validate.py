"""Checks one Code Tutor answer: same six parts, pictures that the app can really draw, code that compiles.
Used to filter generated training data and to score a trained model (eval_tutor.py)."""
import ast
import json
import re

HEADINGS = ["Idea", "Visual", "Code", "Step by step", "Common mistake", "Try it"]
VISUALS = {"flow", "chart", "array", "vars", "svg", "sim", "complexity", "network"}
SIM_ALGOS = {"bubble_sort": 12, "selection_sort": 12, "insertion_sort": 12, "linear_search": 20, "binary_search": 20, "factorial": 0}
CURVES = {"1", "log n", "n", "n log n", "n^2", "2^n"}
LIST_LITERAL = re.compile(r"\[\s*-?\d+(?:\s*,\s*-?\d+){2,}\s*\]")
FENCE = re.compile(r"```([A-Za-z0-9+#_-]*)[ \t]*\n(.*?)```", re.S)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")


def parse_flow(src: str) -> list[tuple[str, str, str]]:
    """Same rule as the app: 'A -> B -(label)-> C' per line."""
    edges = []
    for line in src.splitlines():
        p = re.split(r"\s*-(?:\(([^)]*)\)-)?>\s*", line.strip())
        for i in range(0, len(p) - 2, 2):
            a, b = p[i].strip(), p[i + 2].strip()
            if a and b and a != b:
                edges.append((a, b, p[i + 1] or ""))
    return edges


def check_visual(lang: str, body: str) -> str | None:
    try:
        if lang == "flow":
            e = parse_flow(body)
            names = {x for a, b, _ in e for x in (a, b)}
            return None if e and len(names) <= 20 else "flow needs 1+ arrows and at most 20 boxes"
        if lang == "svg":
            ok = body.lstrip().startswith("<svg") and len(body) <= 40000 and not re.search(r"<script|onload|onclick|javascript:", body, re.I)
            return None if ok else "svg must start with <svg>, stay under 40000 chars, no scripts"
        o = json.loads(body)
        if lang == "chart":
            x, y = o.get("x") or o.get("labels") or [], o.get("y") or o.get("values") or []
            ok = 1 <= len(x) <= 24 and len(x) == len(y) and all(isinstance(v, (int, float)) for v in y)
            return None if ok else "chart: x and y must be same length (1 to 24), y numbers"
        if lang == "array":
            it = o.get("items") or []
            n = len(it)
            ptr = o.get("pointers") or {}
            hi = o.get("highlight") or []
            ok = 1 <= n <= 16 and all(isinstance(v, int) and 0 <= v < n for v in list(ptr.values()) + list(hi))
            return None if ok else "array: 1 to 16 items, pointers/highlight must be valid indexes"
        if lang == "vars":
            v = o.get("vars") or []
            names = {i.get("name") for i in v if isinstance(i, dict) and "value" in i}
            ok = 1 <= len(v) <= 8 and all(isinstance(i, dict) and "name" in i and ("value" in i or i.get("same_as") in names) for i in v)
            return None if ok else "vars: 1 to 8 entries; each needs a value, or same_as naming another entry"
        if lang == "network":
            layers = o.get("layers")
            if not isinstance(layers, list) or not 1 <= len(layers) <= 6:
                return "network: 1 to 6 layers"
            for ly in layers:
                nodes = ly.get("nodes") if isinstance(ly, dict) else None
                if not isinstance(nodes, list) or not 1 <= len(nodes) <= 8 or not all(isinstance(n, str) and 0 < len(n) <= 12 for n in nodes):
                    return "network: each layer needs 1 to 8 node names of at most 12 characters"
            for key in ("inputs", "outputs"):
                v = o.get(key)
                if v is not None and (not isinstance(v, list) or len(v) > 8 or not all(isinstance(x, str) for x in v)):
                    return f"network: {key} must be a list of up to 8 names"
            return None
        if lang == "sim":
            algo = o.get("algo")
            if algo not in SIM_ALGOS:
                return "sim: unknown algo"
            whole = lambda x: isinstance(x, int) and not isinstance(x, bool) and abs(x) <= 999
            if algo == "factorial":
                n = o.get("n")
                return None if isinstance(n, int) and not isinstance(n, bool) and 0 <= n <= 12 else "sim factorial: n must be a whole number from 0 to 12"
            lst = o.get("input")
            if not isinstance(lst, list) or not 1 <= len(lst) <= SIM_ALGOS[algo] or not all(whole(x) for x in lst):
                return f"sim {algo}: input must be 1 to {SIM_ALGOS[algo]} whole numbers between -999 and 999"
            if "search" in algo and not whole(o.get("target")):
                return "sim: searches need a whole-number target"
            if algo == "binary_search" and lst != sorted(lst):
                return "sim binary_search: input must be sorted"
            return None
        if lang == "complexity":
            n, cv = o.get("n"), o.get("curves") or ["1", "log n", "n", "n log n", "n^2"]
            ok = isinstance(n, int) and 1 <= n <= 1024 and isinstance(cv, list) and 1 <= len(cv) <= 6 and set(cv) <= CURVES and not ("2^n" in cv and n > 20)
            return None if ok else "complexity: n from 1 to 1024, curves from the allowed list (2^n only for n up to 20)"
    except (ValueError, AttributeError, TypeError):
        return f"{lang}: block is not valid"
    return None


def validate(answer: str, lang: str = "en") -> list[str]:
    """Returns a list of problems (empty list = good)."""
    bad: list[str] = []
    if answer.count("```") % 2:
        return ["a code fence is not closed"]
    if not 500 <= len(answer) <= 7000:
        bad.append(f"length {len(answer)} chars (want 500 to 7000)")
    last = -1
    for h in HEADINGS:
        m = re.search(r"\*\*\s*" + re.escape(h) + r"\s*:?\s*\*\*", answer)
        if not m or m.start() < last:
            bad.append(f"missing or out of order: **{h}**")
        else:
            last = m.start()
    blocks = [(l.lower(), b) for l, b in FENCE.findall(answer)]
    if any(l == "mermaid" for l, _ in blocks):
        bad.append("mermaid is not supported")
    vis = [(l, b) for l, b in blocks if l in VISUALS]
    table = re.search(r"^\|.*\|\s*\n\|[\s:|-]+\|", answer, re.M)
    if not vis and not table:
        bad.append("no picture: add a flow/chart/array/vars block or a table")
    for l, b in vis:
        p = check_visual(l, b)
        if p:
            bad.append(p)
    if any(l == "sim" for l, _ in vis):  # a sim shows every step itself: hand-written traces next to it can be wrong
        m = re.search(r"\*\*\s*Step by step\s*:?\s*\*\*(.*?)(?=\*\*\s*Common mistake|\Z)", answer, re.S)
        if m and LIST_LITERAL.search(m.group(1)):
            bad.append("Step by step lists intermediate lists: let the sim show the steps")
    code = [(l, b) for l, b in blocks if l and l not in VISUALS]
    if not code:
        bad.append("no code block with a language tag")
    for l, b in code:
        if l in ("python", "py"):
            try:
                ast.parse(b)
            except SyntaxError as e:
                bad.append(f"python code does not compile: {e.msg} (line {e.lineno})")
    if lang == "hinglish" and DEVANAGARI.search(answer):  # Roman Hinglish must not use Devanagari
        bad.append("Roman Hinglish answer contains Devanagari")
    return bad
