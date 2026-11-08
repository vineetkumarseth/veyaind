"""Shared test setup: a throw-away data folder, set BEFORE main.py is imported."""
import os
import sys
import tempfile

_TMP = tempfile.mkdtemp(prefix="veya_test_")
os.environ["VEYA_DATA_DIR"] = _TMP
os.environ.setdefault("VEYA_DAILY_CREDITS", "5")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import main  # noqa: E402  (imported after the environment is prepared)
from fastapi import BackgroundTasks  # noqa: E402


def new_user(name="Test"):
    key = main.create_user(name)
    with main.db() as con:
        uid = con.execute("SELECT user_id FROM api_keys WHERE key_hash = ?", (main.hash_key(key),)).fetchone()["user_id"]
    return {"id": uid, "name": name}, key


def bg():
    return BackgroundTasks()
