"""Auto web search, the thinking/process events, drawing in every mode, and photo attachments."""
import unittest

from .common import bg, main, new_user


class Patched(unittest.TestCase):
    def setUp(self):
        self.saved = {k: getattr(main, k) for k in ("embed", "recall", "doc_search", "ollama", "ollama_stream", "installed_models", "fetch_weather", "search_provider", "web_context")}
        self.payloads, self.web_calls = [], []
        main.embed = lambda t: [1.0]
        main.recall = lambda *a, **k: []
        main.doc_search = lambda *a, **k: []
        main.installed_models = lambda: ["qwen3:8b"]
        main.fetch_weather = lambda m: None
        main.search_provider = lambda: "tavily"

        def fake_web(uid, message, model, emit=None):
            self.web_calls.append(message)
            if emit:
                emit("s", "Searching the web for: " + message)
                emit("s", "Reading 3 search results")
            return "\nWeb search results (fake)\n[1] Sensex 1,000 (https://example.com): 1,000", ["Web search (tavily)"], [{"title": "t", "url": "https://example.com", "snippet": "s"}], ""
        main.web_context = fake_web

        def fake_chat(path, payload, timeout=180):
            self.payloads.append(payload)
            return {"message": {"content": "answer 1000", "thinking": "I should check the numbers."}}
        main.ollama = fake_chat

        def fake_stream(payload, on_token, on_think=None):
            self.payloads.append(payload)
            for t in ("The Sensex ", "is 1,000."):
                on_token(t)
            if on_think:
                on_think("Let me look at the results. ")
            return {"message": {"content": "The Sensex is 1,000.", "thinking": "Let me look at the results. "}}
        main.ollama_stream = fake_stream

    def tearDown(self):
        for k, v in self.saved.items():
            setattr(main, k, v)


class AutoWeb(Patched):
    def test_manual_by_default_no_search_unless_the_user_asks(self):
        u, _ = new_user("aw0")
        out = main.respond(u["id"], "What is the sensex today?", bg())
        self.assertEqual(self.web_calls, [])                             # nothing is searched on its own
        self.assertIn("Web button", out["reply"])
        self.assertTrue(out["offer_web"])                                 # the UI shows a one-tap "Search the web" button
        out = main.respond(u["id"], "What is the sensex today?", bg(), web=True)   # the user turned Web on
        self.assertEqual(len(self.web_calls), 1)
        self.assertTrue(out["web_sources"])
        self.assertIn("The Web button is on", out["process"]["steps"][1] if len(out["process"]["steps"]) > 1 else "")

    def test_conceptual_question_never_searches_even_with_auto_on(self):
        u, _ = new_user("aw0b")
        main.respond(u["id"], "Explain auto associative and hetero associative networks.", bg(), auto_web_opt=True)
        self.assertEqual(self.web_calls, [])

    def test_opt_in_auto_search(self):
        u, _ = new_user("aw1")
        out = main.respond(u["id"], "What is the sensex today?", bg(), auto_web_opt=True)
        self.assertEqual(len(self.web_calls), 1)
        self.assertNotIn("do not have live data", out["reply"].lower())
        self.assertTrue(out["web_sources"])

    def test_normal_and_tutor_questions_do_not_search(self):
        u, _ = new_user("aw2")
        main.respond(u["id"], "Explain learning rate in gradient descent.", bg(), auto_web_opt=True)
        main.respond(u["id"], "What is the latest news in my own code review today?", bg(), mode="tutor", auto_web_opt=True)
        self.assertEqual(self.web_calls, [])

    def test_detector(self):
        yes = ["What is the latest version of Python?", "Who is the current CEO of Google?", "ipl score aaj", "Bitcoin price today", "aaj ki taaza khabar"]
        no = ["Explain recursion", "What is learning rate?", "Write a for loop", "current in a circuit is measured in amperes", "How do I sort a list?"]
        for m in yes:
            self.assertTrue(main.needs_fresh_info(m), m)
        for m in no:
            self.assertFalse(main.needs_fresh_info(m), m)

    def test_without_a_search_key_the_gate_stays_honest(self):
        main.search_provider = lambda: ""
        u, _ = new_user("aw3")
        out = main.respond(u["id"], "What is the sensex today?", bg())
        self.assertIn("live data", out["reply"].lower())
        self.assertEqual(self.web_calls, [])

    def test_admin_can_forbid_auto_search(self):
        old = main.AUTO_WEB
        main.AUTO_WEB = False
        try:
            u, _ = new_user("aw4")
            out = main.respond(u["id"], "What is the sensex today?", bg(), auto_web_opt=True)
            self.assertEqual(self.web_calls, [])
            self.assertIn("Web button", out["reply"])
        finally:
            main.AUTO_WEB = old


class Process(Patched):
    def test_steps_arrive_in_order_and_are_saved(self):
        u, _ = new_user("pr1")
        seen = []
        out = main.respond(u["id"], "What is the sensex today?", bg(), web=True, on_token=lambda t: None, on_event=lambda k, t: seen.append((k, t)))
        steps = [t for k, t in seen if k == "s"]
        self.assertEqual(steps[0], "Reading your question")
        self.assertIn("Searching the web for: What is the sensex today?", steps)
        self.assertEqual(steps[-1], "Writing the answer")
        self.assertIn(("t", "Let me look at the results. "), seen)        # the model's reasoning is streamed too
        self.assertEqual(out["process"]["steps"], steps)
        self.assertIn("results", out["process"]["thinking"])
        h = main.history(out["chat_id"], u)
        self.assertEqual(h[-1]["meta"]["process"]["steps"], steps)         # and kept in the history

    def test_non_streaming_path_still_reports_steps(self):
        u, _ = new_user("pr2")
        out = main.respond(u["id"], "Explain recursion", bg())
        self.assertEqual(out["process"]["steps"][0], "Reading your question")
        self.assertEqual(out["process"]["thinking"], "I should check the numbers.")


class DrawingAndPhotos(Patched):
    def test_every_mode_can_draw_the_tutor_has_its_own_rules(self):
        u, _ = new_user("dr1")
        main.respond(u["id"], "Draw an associative memory network", bg())
        self.assertIn("```network", self.payloads[-1]["messages"][0]["content"])
        main.respond(u["id"], "Teach me recursion", bg(), mode="tutor")
        system = self.payloads[-1]["messages"][0]["content"]
        self.assertNotIn("Never say that you cannot draw", system)         # not duplicated in tutor mode
        self.assertIn("```sim", system)

    def test_photo_thumbnails_are_stored_with_the_message_and_cleaned(self):
        u, _ = new_user("ph1")
        main.installed_models = lambda: ["qwen3:8b", "llava:latest"]   # a photo needs a vision model
        good = "data:image/jpeg;base64," + "A" * 200
        out = main.respond(u["id"], "give me this type of architecture", bg(), images=["data:image/jpeg;base64,QUJD"], thumbs=[good, "data:text/html;base64,PHNjcmlwdD4=", "x" * 10, "data:image/jpeg;base64," + "B" * 200000])
        h = main.history(out["chat_id"], u)
        user_msg = [m for m in h if m["role"] == "user"][0]
        self.assertEqual([a["thumb"] for a in user_msg["meta"]["attachments"]], [good])   # only the safe, small JPEG was kept
        self.assertTrue(user_msg["content"].endswith("[photo attached]"))               # the model's context still knows a photo was there

    def test_no_attachment_meta_without_photos(self):
        u, _ = new_user("ph2")
        out = main.respond(u["id"], "hello", bg())
        user_msg = [m for m in main.history(out["chat_id"], u) if m["role"] == "user"][0]
        self.assertNotIn("attachments", user_msg["meta"])


if __name__ == "__main__":
    unittest.main()
