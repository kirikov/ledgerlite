import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "ledger.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, "
            "category TEXT NOT NULL, amount_cents INTEGER NOT NULL, note TEXT, created_at TEXT NOT NULL)"
        )
