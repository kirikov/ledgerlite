from flask import Flask, jsonify, request

from . import service
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
