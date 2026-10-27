from datetime import datetime, timezone

from .db import connect


def add_expense(owner: str, category: str, amount_cents: int, note: str | None = None) -> int:
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO expenses (owner, category, amount_cents, note, created_at) VALUES (?, ?, ?, ?, ?)",
            (owner, category, amount_cents, note, datetime.now(timezone.utc).isoformat()),
        )
        return int(cur.lastrowid)


def list_expenses(owner: str, page: int = 1, page_size: int = 20) -> list[dict]:
    offset = (page - 1) * page_size
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE owner = ? ORDER BY id LIMIT ? OFFSET ?",
            (owner, page_size, offset),
        ).fetchall()
    return [dict(r) for r in rows]


def total_cents(owner: str) -> int:
    with connect() as conn:
        row = conn.execute("SELECT COALESCE(SUM(amount_cents), 0) AS t FROM expenses WHERE owner = ?", (owner,)).fetchone()
    return int(row["t"])
