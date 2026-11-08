"""Tutor continuity, the shared prompt, and the regression suite's own checkers. Run: python -m unittest discover -s tests -v"""
import os
import re
import sys
import unittest

from .common import bg, main, new_user

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tutor"))
sys.path.insert(0, os.path.join(ROOT, "eval", "tutor_regression"))
import tutor_prompt  # noqa: E402
from validate import FENCE, check_visual  # noqa: E402


class TutorContinuity(unittest.TestCase):
    def test_objective_and_language_survive_a_short_reply(self):
        saved = {k: getattr(main, k) for k in ("embed", "recall", "doc_search", "ollama", "installed_models", "fetch_weather")}
        seen = []
        main.embed = lambda t: [1.0]
        main.recall = lambda *a, **k: []
        main.doc_search = lambda *a, **k: []
        main.installed_models = lambda: ["qwen3:8b"]
        main.fetch_weather = lambda m: None
        main.ollama = lambda path, payload, timeout=180: seen.append(payload) or {"message": {"content": "ok"}}
        try:
            u, _ = new_user("cont")
            first = main.respond(u["id"], "Hinglish me samjhao: for loop kya hota hai? Mujhe sikhao.", bg(), mode="tutor")
            main.respond(u["id"], "I think it prints 1 2 3", bg(), mode="tutor", chat_id=first["chat_id"])
            system = seen[-1]["messages"][0]["content"]
            self.assertIn("Current learning objective", system)
            self.assertIn("for loop", system)                       # the topic from the start of the chat is kept
            self.assertIn("Roman Hinglish", system)                 # the chat language is kept even though the last message is English
            self.assertIn("Quiz and practice rules", system)
            self.assertNotIn("What you know about this user", system)
        finally:
            for k, v in saved.items():
                setattr(main, k, v)


class PromptContract(unittest.TestCase):
    def test_every_example_block_in_the_prompt_is_a_valid_spec(self):
        blocks = FENCE.findall(tutor_prompt.TUTOR_PROMPT)
        kinds = {l for l, _ in blocks}
        self.assertTrue({"flow", "sim", "complexity", "vars", "array"} <= kinds)
        for lang, body in blocks:
            self.assertIsNone(check_visual(lang, body), (lang, body))

    def test_fact_guardrails_are_present(self):
        p = tutor_prompt.TUTOR_PROMPT
        for needle in ("name that points to an object", "XOR", "hidden layer", "encoder-decoder", "decoder-only", "factorial(0) is 1", "one question at a time"):
            self.assertIn(needle, p)

    def test_app_and_kit_use_the_same_prompt(self):
        self.assertIn(tutor_prompt.TUTOR_PROMPT, main.MODES["tutor"])


class RegressionSuite(unittest.TestCase):
    def test_suite_shape(self):
        from cases import CASES
        self.assertGreaterEqual(len(CASES), 50)
        cats = {c["category"] for c in CASES}
        for need in ("Python fundamentals", "Loops and conditions", "Recursion", "Data structures", "Sorting and searching", "SQL", "Operating systems",
                     "Neural networks", "Transformers", "Debugging", "Visual correctness", "Adaptive tutoring", "Privacy and context"):
            self.assertIn(need, cats)
        for c in CASES:
            for key in ("require", "forbid"):
                for rx in c.get(key, []):
                    re.compile(rx)
            for grp in c.get("require_any", []):
                for rx in grp:
                    re.compile(rx)

    def test_checkers_catch_what_they_should(self):
        import run_regression
        self.assertTrue(run_regression.selftest())


if __name__ == "__main__":
    unittest.main()
