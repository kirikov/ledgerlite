from flask import Flask, jsonify, request

from datetime import date

from . import export, service
from .db import init_db

app = Flask(__name__)
init_db()


@app.post("/expenses")
def create():
    body = request.get_json(force=True)
    expense_id = service.add_expense(body["owner"], body["category"], int(body["amount_cents"]), body.get("note"))
    return jsonify({"id": expense_id}), 201


@app.get("/expenses")
def index():
    owner = request.args["owner"]
    page = int(request.args.get("page", 1))
    return jsonify(service.list_expenses(owner, page))


@app.get("/expenses/total")
def total():
    return jsonify({"owner": request.args["owner"], "total_cents": service.total_cents(request.args["owner"])})


@app.get("/expenses/export")
def export_csv():
    if request.args.get("token") != export.EXPORT_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    owner = request.args["owner"]
    category = request.args.get("category")
    since = date.fromisoformat(request.args["since"]) if request.args.get("since") else None
    rows = export.rows_for_export(owner, category, since)
    path = export.write_export_file(owner, export.to_csv(rows))
    return jsonify({"rows": len(rows), "file": path, "monthly": export.monthly_totals(rows)})
