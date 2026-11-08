"""VEYRA modes, waitlist, credits, privacy and code checks. Run:  python -m unittest discover -s tests -v
These call the server functions directly (no Ollama needed)."""
import json
import sqlite3
import time
import unittest

from fastapi import HTTPException

from .common import bg, main, new_user
import veyra_modes
import migrations


class Modes(unittest.TestCase):
    def test_only_core_is_available(self):
        m = veyra_modes.all_modes()
        self.assertEqual([k for k, v in m.items() if v.available], ["core"])
        self.assertEqual(m["deep"].status, "waitlist")
        self.assertEqual(m["flash"].status, "waitlist")

    def test_public_view_hides_internals(self):
        for m in veyra_modes.all_modes().values():
            self.assertFalse({"adapter", "generation", "context_budget", "tools", "restrictions"} & set(m.public()))

    def test_core_runs_qwen3_8b_by_default(self):
        self.assertEqual(veyra_modes.get("core").adapter["model"], "qwen3:8b")

    def test_release_needs_switch_and_a_model(self):
        import os
        os.environ["VEYA_MODE_DEEP"] = "available"
        try:
            self.assertEqual(veyra_modes.get("deep").status, "waitlist")        # switched on but no checkpoint: still locked
            os.environ["VEYA_DEEP_MODEL"] = "veyra-deep:test"
            self.assertEqual(veyra_modes.get("deep").status, "available")
        finally:
            os.environ.pop("VEYA_MODE_DEEP", None)
            os.environ.pop("VEYA_DEEP_MODEL", None)
        self.assertEqual(veyra_modes.get("deep").status, "waitlist")


class Gate(unittest.TestCase):
    def test_server_side_gate(self):
        self.assertEqual(main.veyra_or_http(None).id, "core")
        self.assertEqual(main.veyra_or_http("CORE").id, "core")
        for locked in ("deep", "flash"):
            with self.assertRaises(HTTPException) as c:
                main.veyra_or_http(locked)
            self.assertEqual(c.exception.status_code, 403)
        with self.assertRaises(HTTPException) as c:
            main.veyra_or_http("turbo")
        self.assertEqual(c.exception.status_code, 400)

    def test_locked_mode_costs_nothing_and_never_reaches_the_model(self):
        user, _ = new_user("gate")
        called = []
        original = main._respond
        main._respond = lambda *a, **k: called.append(1) or {"reply": "x"}
        try:
            for locked in ("deep", "flash", "nonsense"):
                with self.assertRaises(HTTPException):
                    main.respond(user["id"], "hello", bg(), veyra=locked)
        finally:
            main._respond = original
        self.assertEqual(called, [])
        self.assertEqual(main.studio_used(user["id"], "chat"), 0)

    def test_core_charges_credits_and_refunds_on_failure(self):
        user, _ = new_user("credits")
        original = main._respond
        main._respond = lambda *a, **k: {"reply": "ok"}
        try:
            main.respond(user["id"], "hi", bg(), veyra="core")
            self.assertEqual(main.studio_used(user["id"], "chat"), 1)
            main._respond = lambda *a, **k: (_ for _ in ()).throw(HTTPException(503, "Ollama is down"))
            with self.assertRaises(HTTPException):
                main.respond(user["id"], "hi", bg(), veyra="core")
            self.assertEqual(main.studio_used(user["id"], "chat"), 1)   # refunded
        finally:
            main._respond = original

    def test_daily_limit_blocks(self):
        user, _ = new_user("limit")
        original = main._respond
        main._respond = lambda *a, **k: {"reply": "ok"}
        try:
            for _ in range(main.DAILY_CREDITS):
                main.respond(user["id"], "hi", bg())
            with self.assertRaises(HTTPException) as c:
                main.respond(user["id"], "hi", bg())
            self.assertEqual(c.exception.status_code, 429)
        finally:
            main._respond = original


class Waitlist(unittest.TestCase):
    def test_join_duplicate_leave(self):
        u, _ = new_user("wl")
        a = main.veyra_join(main.VeyraWaitIn(mode="deep"), u)
        self.assertTrue(a["ok"])
        self.assertFalse(a["already_registered"])
        b = main.veyra_join(main.VeyraWaitIn(mode="deep"), u)
        self.assertTrue(b["already_registered"])
        self.assertEqual(a["registered_at"], b["registered_at"])           # date of the first registration is kept
        with main.db() as con:
            n = con.execute("SELECT COUNT(*) FROM model_waitlist WHERE user_id = ? AND mode_id = 'deep'", (u["id"],)).fetchone()[0]
        self.assertEqual(n, 1)
        self.assertTrue(main.veyra_leave("deep", u)["removed"])
        self.assertFalse(main.veyra_leave("deep", u)["removed"])

    def test_validation(self):
        u, _ = new_user("val")
        with self.assertRaises(HTTPException) as c:
            main.veyra_join(main.VeyraWaitIn(mode="turbo"), u)
        self.assertEqual(c.exception.status_code, 400)
        with self.assertRaises(HTTPException) as c:
            main.veyra_join(main.VeyraWaitIn(mode="core"), u)             # nothing to wait for
        self.assertEqual(c.exception.status_code, 400)
        with self.assertRaises(HTTPException):
            main.veyra_leave("turbo", u)

    def test_registrations_are_user_scoped(self):
        a, _ = new_user("alice")
        b, _ = new_user("bob")
        main.veyra_join(main.VeyraWaitIn(mode="flash"), a)
        listing_a = {m["id"]: m for m in main.veyra_list(a)["modes"]}
        listing_b = {m["id"]: m for m in main.veyra_list(b)["modes"]}
        self.assertTrue(listing_a["flash"]["waitlisted"])
        self.assertFalse(listing_b["flash"]["waitlisted"])
        self.assertFalse(main.veyra_leave("flash", b)["removed"])           # bob cannot remove alice's registration
        self.assertTrue(main.veyra_list(a)["modes"][2]["waitlisted"])

    def test_listing_shape(self):
        u, _ = new_user("shape")
        out = main.veyra_list(u)
        self.assertEqual((out["brand"], out["foundation"], out["default"]), ("VEYRA", "Qwen3-8B", "core"))
        self.assertEqual([m["id"] for m in out["modes"]], ["core", "deep", "flash"])
        self.assertTrue(out["modes"][0]["selectable"])
        self.assertFalse(out["modes"][1]["selectable"] or out["modes"][2]["selectable"])


class Migrations(unittest.TestCase):
    def test_idempotent_and_keeps_old_data(self):
        con = sqlite3.connect(":memory:")
        con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")      # an "older Veya" database
        con.execute("INSERT INTO users (name) VALUES ('keep me')")
        self.assertEqual(migrations.migrate(con), [1, 2, 3])
        self.assertEqual(migrations.migrate(con), [])
        self.assertEqual(con.execute("SELECT name FROM users").fetchone()[0], "keep me")
        con.execute("INSERT INTO model_waitlist (user_id, mode_id, created_at) VALUES (1,'deep',0)")
        with self.assertRaises(sqlite3.IntegrityError):
            con.execute("INSERT INTO model_waitlist (user_id, mode_id, created_at) VALUES (1,'deep',1)")


class Privacy(unittest.TestCase):
    def _patch(self):
        self.saved = {k: getattr(main, k) for k in ("embed", "recall", "doc_search", "ollama", "installed_models", "fetch_weather", "check_code_blocks")}
        self.recalled = []
        main.embed = lambda t: [1.0, 0.0]
        main.recall = lambda uid, qv, k=3: self.recalled.append(1) or ["The user is a B.Tech student at SECRET COLLEGE."]
        main.doc_search = lambda uid, qv, k=4: []
        main.installed_models = lambda: ["qwen3:8b"]
        main.fetch_weather = lambda m: None
        main.ollama = lambda path, payload, timeout=180: {"message": {"content": "Here is the answer."}}

    def _unpatch(self):
        for k, v in self.saved.items():
            setattr(main, k, v)

    def test_tutor_mode_ignores_personal_memory_and_learns_nothing(self):
        self._patch()
        try:
            u, _ = new_user("tut")
            tasks = bg()
            out = main.respond(u["id"], "Teach me recursion", tasks, mode="tutor")
            self.assertEqual(self.recalled, [])                              # memories were not even looked up
            self.assertEqual(tasks.tasks if hasattr(tasks, "tasks") else tasks.t, [])   # no "learn" task: no facts written from tutoring
            self.assertEqual(out["memories_n"], 0)
        finally:
            self._unpatch()

    def test_normal_chat_hides_memory_text_by_default(self):
        self._patch()
        try:
            u, _ = new_user("norm")
            out = main.respond(u["id"], "What should I study?", bg())
            self.assertEqual(out["memories_used"], [])                      # text hidden
            self.assertEqual(out["memories_n"], 1)                          # only a count
            with main.db() as con:
                meta = con.execute("SELECT meta FROM messages WHERE user_id = ? AND role = 'assistant'", (u["id"],)).fetchone()["meta"]
            stored = main.dec(meta)
            self.assertNotIn("SECRET COLLEGE", stored)                      # not persisted next to the message either
            opted = main.respond(u["id"], "What should I study?", bg(), show_context=True)
            self.assertIn("SECRET COLLEGE", opted["memories_used"][0])
        finally:
            self._unpatch()

    def test_documents_are_isolated_per_user(self):
        a, _ = new_user("docA")
        b, _ = new_user("docB")
        for user, text in ((a, "alice private notes"), (b, "bob private notes")):
            with main.db() as con:
                did = con.execute("INSERT INTO docs (user_id, name, chunks, ts) VALUES (?,?,?,?)", (user["id"], main.enc("notes.txt"), 1, 0)).lastrowid
                con.execute("INSERT INTO doc_chunks (doc_id, user_id, text, emb) VALUES (?,?,?,?)", (did, user["id"], main.enc(text), json.dumps([1.0, 0.0])))
            user["doc"] = did
        got_b = [t for t, _ in main.doc_search(b["id"], [1.0, 0.0])]
        self.assertEqual(got_b, ["bob private notes"])
        self.assertEqual(main.doc_text(b["id"], a["doc"]), "")              # cannot read another user's file by id

    def test_consent_defaults_off_and_guards_training_export(self):
        u, _ = new_user("consent")
        self.assertFalse(main.training_export_allowed(u["id"]))
        main.consents_set(main.ConsentIn(scope="model_training", granted=True), u)
        self.assertTrue(main.training_export_allowed(u["id"]))
        main.consents_set(main.ConsentIn(scope="model_training", granted=False), u)
        self.assertFalse(main.training_export_allowed(u["id"]))
        with self.assertRaises(HTTPException):
            main.consents_set(main.ConsentIn(scope="everything", granted=True), u)

    def test_old_history_memory_text_is_not_returned(self):
        u, _ = new_user("hist")
        cid = main.get_chat(u["id"], 0, "hello")
        main.save_msg(u["id"], "assistant", "hi", cid, {"memories_used": ["The user lives at 12 Secret Street"]})
        out = main.history(cid, u)
        self.assertNotIn("Secret Street", json.dumps(out))
        self.assertEqual(out[0]["meta"]["memories_n"], 1)


class CodeChecks(unittest.TestCase):
    REPLY = "text\n```python\nprint(1+1)\n```\nmore\n```python\nx = input()\n```\n"

    def test_not_run_when_execution_is_off(self):
        old = main.ALLOW_RUN
        main.ALLOW_RUN = False
        try:
            r = main.check_code_blocks(self.REPLY)
            self.assertEqual([c["status"] for c in r], ["not_run", "not_run"])
        finally:
            main.ALLOW_RUN = old

    def test_real_statuses_when_allowed(self):
        old, run = main.ALLOW_RUN, main.run_python
        main.ALLOW_RUN = True
        try:
            main.run_python = lambda code, timeout=10: (True, "2\n")
            r = main.check_code_blocks(self.REPLY)
            self.assertEqual([c["status"] for c in r], ["passed", "not_run"])   # input() is never run
            main.run_python = lambda code, timeout=10: (False, "NameError")
            self.assertEqual(main.check_code_blocks("```python\nprint(x)\n```")[0]["status"], "failed")
            main.run_python = lambda code, timeout=10: (None, "no sandbox")
            self.assertEqual(main.check_code_blocks("```python\npass\n```")[0]["status"], "not_run")
        finally:
            main.ALLOW_RUN, main.run_python = old, run


if __name__ == "__main__":
    unittest.main()
