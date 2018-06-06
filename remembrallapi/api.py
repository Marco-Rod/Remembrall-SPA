"""
Provides the API endpoints for consuming and producing
REST requests and responses
"""

from flask import Blueprint, jsonify, request, abort
from remembrallapi.models import db, User, Plan, Payment, PlanUser

api = Blueprint("api", __name__)


@api.route("/users", methods=["GET", "POST"])
def fetch_users():
    if request.method == "GET":
        obj = {}
        url = '/users'
        start = int(request.args.get('start', 1))
        limit = int(request.args.get('limit', 20))
        users = User.query.all()
        count = len(users)
        if (count < start):
            return jsonify(obj)
        obj["start"] = start
        obj["limit"] = limit
        obj["count"] = 1
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj['previous'] = url + \
                '?start=%d&limit=%d' % (start_copy, limit_copy)
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        users_data = [u.to_dict() for u in users]
        obj["users"] = users_data[(start - 1):(start - 1 + limit)]
        return jsonify(obj)

    elif request.method == "POST":
        data = request.get_json()
        user = User(
            name=data["name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            avatar=data["avatar"],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201


@api.route("/user/<int:id>/", methods=["GET"])
def user(id):
    user = User.query.get(id)
    return jsonify({"user": user.to_dict()})


@api.route("/plans", methods=["GET", "POST"])
def fetch_plans():
    if request.method == "GET":
        plans = Plan.query.all()
        return jsonify({"plans": [p.to_dict() for p in plans]})


@api.route("/plan/<int:id>/", methods=["GET"])
def plan(id):
    plan = Plan.query.get(id)
    return jsonify({"plan": plan.to_dict()})


@api.route("/payments", methods=["GET", "POST"])
def fetch_pays():
    if request.method == "GET":
        payments = Payment.query.all()
        return jsonify({"payments": [p.to_dict() for p in payments]})


@api.route("/payment/<int:id>/", methods=["GET"])
def pay(id):
    payment = Payment.query.get(id)
    return jsonify({"payment": pay.to_dict()})
