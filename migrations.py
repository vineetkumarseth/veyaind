"""Tiny versioned migrations for Veya's SQLite database.

Older Veya versions create their tables with inline CREATE TABLE IF NOT EXISTS. This runner adds a schema_migrations
table, records version 1 as the baseline (those older tables), and then applies each newer step exactly once.
Every statement is idempotent, so running it twice, or on a database from an older Veya, is safe."""
import time

MIGRATIONS = [
    (1, "baseline: tables created by earlier Veya versions", []),
    (2, "veyra model waitlist", [
        """CREATE TABLE IF NOT EXISTS model_waitlist (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               mode_id TEXT NOT NULL,
               created_at REAL NOT NULL,
               UNIQUE (user_id, mode_id))""",
        "CREATE INDEX IF NOT EXISTS idx_model_waitlist_user ON model_waitlist (user_id)",
    ]),
    (3, "consents (training use of student data is opt-in)", [
        """CREATE TABLE IF NOT EXISTS consents (
               user_id INTEGER NOT NULL,
               scope TEXT NOT NULL,
               granted INTEGER NOT NULL,
               updated_at REAL NOT NULL,
               PRIMARY KEY (user_id, scope))""",
    ]),
]


def migrate(con) -> list:
    """Apply missing migrations. Returns the versions applied in this call."""
    con.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL, applied_at REAL NOT NULL)")
    done = {r[0] for r in con.execute("SELECT version FROM schema_migrations")}
    applied = []
    for version, name, statements in MIGRATIONS:
        if version in done:
            continue
        for sql in statements:
            con.execute(sql)
        con.execute("INSERT INTO schema_migrations (version, name, applied_at) VALUES (?,?,?)", (version, name, time.time()))
        applied.append(version)
    con.commit()
    return applied
