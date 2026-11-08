"""HTTP-level checks of the VEYRA endpoints with FastAPI's TestClient. Needs the real fastapi and httpx (pip install -r requirements.txt).
They are skipped automatically where those are not installed."""
import unittest

try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    TestClient = None

from .common import main, new_user


@unittest.skipUnless(TestClient, "needs the real fastapi + httpx")
class VeyraHttp(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(main.app)
        _, key = new_user("http")
        self.h = {"Authorization": "Bearer " + key, "X-Requested-With": "veya"}

    def test_requires_login(self):
        self.assertEqual(self.c.get("/v1/veyra/modes").status_code, 401)

    def test_modes_listing(self):
        r = self.c.get("/v1/veyra/modes", headers=self.h)
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertEqual([m["id"] for m in d["modes"]], ["core", "deep", "flash"])
        self.assertTrue(d["modes"][0]["selectable"])
        self.assertNotIn("adapter", d["modes"][0])

    def test_waitlisted_mode_is_refused_by_both_chat_endpoints(self):
        for path in ("/v1/chat", "/v1/chat/stream"):
            r = self.c.post(path, headers=self.h, json={"message": "hi", "veyra": "deep"})
            self.assertEqual(r.status_code, 403, path)
            self.assertIn("not available", r.json()["detail"])
        self.assertEqual(self.c.post("/v1/chat", headers=self.h, json={"message": "hi", "veyra": "turbo"}).status_code, 400)

    def test_waitlist_validation_and_flow(self):
        self.assertEqual(self.c.post("/v1/veyra/waitlist", headers=self.h, json={}).status_code, 422)
        self.assertEqual(self.c.post("/v1/veyra/waitlist", headers=self.h, json={"mode": "x" * 40}).status_code, 422)
        self.assertEqual(self.c.post("/v1/veyra/waitlist", headers=self.h, json={"mode": "core"}).status_code, 400)
        a = self.c.post("/v1/veyra/waitlist", headers=self.h, json={"mode": "flash"}).json()
        b = self.c.post("/v1/veyra/waitlist", headers=self.h, json={"mode": "flash"}).json()
        self.assertFalse(a["already_registered"])
        self.assertTrue(b["already_registered"])
        self.assertTrue(self.c.delete("/v1/veyra/waitlist/flash", headers=self.h).json()["removed"])


if __name__ == "__main__":
    unittest.main()
