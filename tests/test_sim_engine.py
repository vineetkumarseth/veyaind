"""Checks the browser's simulation engine against trusted Python references. Needs Node. Run: python -m unittest discover -s tests -v
Every step the player shows comes from this engine, so these tests are what makes the animations trustworthy."""
import json
import math
import os
import random
import shutil
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run_engine(specs):
    p = subprocess.run(["node", os.path.join(HERE, "sim_node.js")], input=json.dumps(specs), capture_output=True, text=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return json.loads(p.stdout)


# ---- independent Python reference algorithms (they count the same operations the same way) ----
def ref_bubble(a):
    a, c, s, n = a[:], 0, 0, len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            c += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                s += 1
                swapped = True
        if not swapped:
            break
    return a, c, s


def ref_selection(a):
    a, c, s, n = a[:], 0, 0, len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            c += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            s += 1
    return a, c, s


def ref_insertion(a):
    a, c, sh = a[:], 0, 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            c += 1
            if a[j] > key:
                a[j + 1] = a[j]
                sh += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, c, sh


@unittest.skipUnless(shutil.which("node"), "Node.js is needed for these tests")
class SimEngine(unittest.TestCase):
    rng = random.Random(2026)

    def lists(self, k=60, maxlen=12):
        out = [[], [5], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [-5, 0, 5, -5, 0], [999, -999]]
        out = [x for x in out if x]
        for _ in range(k):
            out.append([self.rng.randint(-20, 20) for _ in range(self.rng.randint(1, maxlen))])
        return out

    def check_sort_trace(self, res, original):
        steps = res["steps"]
        self.assertEqual(steps[0]["arr"], original)                         # initial state
        self.assertEqual(steps[-1]["arr"], sorted(original))                # final state equals the trusted reference
        self.assertEqual(res["result"], sorted(original))
        prev = steps[0]
        for st in steps[1:]:
            cells = [v for i, v in enumerate(st["arr"]) if i != st["hole"]] + ([st["held"]] if st["held"] is not None else [])
            self.assertEqual(sorted(cells), sorted(original))               # nothing is lost or invented at any step (a lifted key is held aside)
            if st["op"] in ("compare", "keep", "pick", "pass_end", "done", "early", "newmin"):
                self.assertEqual(st["arr"], prev["arr"])                    # these steps never change the list
            for k, v in st["counts"].items():
                self.assertGreaterEqual(v, prev["counts"][k])               # counters only go up
            prev = st

    def test_sorting_matches_references_and_counts(self):
        cases = self.lists()
        for algo, ref in (("bubble_sort", ref_bubble), ("selection_sort", ref_selection), ("insertion_sort", ref_insertion)):
            out = run_engine([{"algo": algo, "input": c} for c in cases])
            for c, res in zip(cases, out):
                self.assertTrue(res["ok"], (algo, c, res))
                self.check_sort_trace(res, c)
                final, comps, other = ref(c)
                self.assertEqual(res["counts"]["comparisons"], comps, (algo, c))
                self.assertEqual(list(res["counts"].values())[1], other, (algo, c))

    def test_bubble_sort_swaps_really_swap_neighbours(self):
        res = run_engine([{"algo": "bubble_sort", "input": [5, 2, 9, 1]}])[0]
        swaps = [i for i, s in enumerate(res["steps"]) if s["op"] == "swap"]
        for i in swaps:
            before, after, (x, y) = res["steps"][i - 1]["arr"], res["steps"][i]["arr"], res["steps"][i]["swap"]
            self.assertEqual(y, x + 1)
            self.assertGreater(before[x], before[y])                        # only swapped because left was bigger
            expect = before[:]
            expect[x], expect[y] = expect[y], expect[x]
            self.assertEqual(after, expect)
        self.assertEqual(res["steps"][-1]["arr"], [1, 2, 5, 9])
        self.assertEqual((res["counts"]["comparisons"], res["counts"]["swaps"]), (6, 4))

    def test_binary_search_every_iteration(self):
        cases = []
        for _ in range(80):
            a = sorted(self.rng.randint(-30, 30) for _ in range(self.rng.randint(1, 20)))
            cases.append((a, self.rng.choice(a + [self.rng.randint(-40, 40)])))
        out = run_engine([{"algo": "binary_search", "input": a, "target": t} for a, t in cases])
        for (a, t), res in zip(cases, out):
            self.assertTrue(res["ok"])
            present = [i for i, v in enumerate(a) if v == t]
            idx = res["result"]
            if present:
                self.assertEqual(a[idx], t)                                 # a correct index
            else:
                self.assertEqual(idx, -1)
            iterations = 0
            for st in res["steps"]:
                if st["op"] == "mid":
                    iterations += 1
                    lo, mid, hi = st["vars"]["low"], st["vars"]["mid"], st["vars"]["high"]
                    self.assertLessEqual(lo, mid)
                    self.assertLessEqual(mid, hi)
                    self.assertEqual(mid, (lo + hi) // 2)
                    if present:                                             # the target is never thrown away
                        self.assertTrue(any(lo <= p <= hi for p in present), (a, t, st))
            self.assertLessEqual(iterations, math.floor(math.log2(len(a))) + 1)   # binary search is logarithmic
            self.assertEqual(res["counts"]["comparisons"], iterations)

    def test_linear_search(self):
        cases = [([4, 8, 15, 16, 23, 42], 23), ([4, 8, 15], 99), ([7], 7), ([2, 2, 2], 2)]
        for (a, t), res in zip(cases, run_engine([{"algo": "linear_search", "input": a, "target": t} for a, t in cases])):
            self.assertEqual(res["result"], a.index(t) if t in a else -1)
            self.assertEqual(res["counts"]["comparisons"], (a.index(t) + 1) if t in a else len(a))

    def test_factorial_all_valid_n_and_boundaries(self):
        out = run_engine([{"algo": "factorial", "n": n} for n in range(0, 13)])
        for n, res in enumerate(out):
            self.assertEqual(res["result"], math.factorial(n))
            self.assertEqual(res["counts"]["calls"], max(n, 1))             # factorial(0) is one call: the base case
            self.assertEqual(res["counts"]["max_depth"], max(n, 1))
            self.assertEqual(res["steps"][-1]["stack"], [])                 # the stack ends empty
            self.assertEqual(sum(1 for s in res["steps"] if s["op"] == "base"), 1)
            returns = [s["ret"] for s in res["steps"] if s["op"] == "return"]
            self.assertEqual(returns[-1], math.factorial(n))
            self.assertEqual(returns, [math.factorial(k) for k in range(1, max(n, 1) + 1)] if n else [1])

    def test_invalid_specs_are_rejected_not_animated(self):
        bad = [{"algo": "factorial", "n": -1}, {"algo": "factorial", "n": 13}, {"algo": "factorial", "n": 2.5}, {"algo": "factorial", "n": "3"},
               {"algo": "binary_search", "input": [3, 1, 2], "target": 1}, {"algo": "binary_search", "input": [1, 2], "target": "x"},
               {"algo": "bubble_sort", "input": []}, {"algo": "bubble_sort", "input": [1, "a"]}, {"algo": "bubble_sort", "input": [1.5, 2]},
               {"algo": "bubble_sort", "input": list(range(13))}, {"algo": "quick_magic", "input": [1]}, {"algo": "bubble_sort", "input": [100000, 1]}, {}]
        for spec, res in zip(bad, run_engine(bad)):
            self.assertFalse(res["ok"], spec)
            self.assertTrue(res["error"])

    def test_complexity_values_are_calculated(self):
        res = run_engine([{"complexity": {"n": 8, "curves": ["1", "log n", "n", "n log n", "n^2"]}}, {"complexity": {"n": 10, "curves": ["2^n"]}},
                          {"complexity": {"n": 30, "curves": ["2^n"]}}, {"complexity": {"n": 0}}, {"complexity": {"n": 8, "curves": ["n^3"]}}])
        self.assertEqual(res[0]["y"], [1, 3, 8, 24, 64])
        self.assertEqual(res[0]["x"], ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)"])
        self.assertEqual(res[1]["y"], [1024])
        self.assertFalse(res[2]["ok"] or res[3]["ok"] or res[4]["ok"])


if __name__ == "__main__":
    unittest.main()
