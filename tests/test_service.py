import os
import tempfile

import app.db as db


def setup_module(module):
    db.DB_PATH = tempfile.mktemp(suffix=".db")
    db.init_db()


def test_add_and_total():
    from app import service
    service.add_expense("ann", "food", 1200)
    service.add_expense("ann", "travel", 800)
    assert service.total_cents("ann") == 2000


def test_pagination():
    from app import service
    for i in range(25):
        service.add_expense("bob", "misc", 100 + i)
    assert len(service.list_expenses("bob", page=1)) == 20
    assert len(service.list_expenses("bob", page=2)) == 5
