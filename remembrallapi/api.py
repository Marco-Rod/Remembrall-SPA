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
        limit = int(request.args.get('limit', 10))
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
        data = request.get_json(silent=True)
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


@api.route("/user/<int:id>/", methods=["GET", "PATCH"])
def user(id):
    if request.method == "GET":
        user = User.query.get(id)
        return jsonify({"user": user.to_dict()})

    elif request.method == "PATCH":
        data = request.get_json()
        user = User.query.get(id)
        user.email = data["email"]
        db.session.commit()
        return jsonify(user.to_dict())

@api.route("/plans", methods=["GET", "POST"])
def fetch_plans():
    if request.method == "GET":
        obj = {}
        url = '/plans'
        start = int(request.args.get('start', 1))
        limit = int(request.args.get('limit', 10))
        plans = Plan.query.all()
        count = len(plans)
        if(count < start):
            return jsonify(obj)
        obj["start"] = start
        obj["limit"] = limit
        obj["count"] = 1
        if start == 1:
            obj["previous"] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj["previous"] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        plans_data = [u.to_dict() for u in plans]
        obj["plans"] = plans_data[(start - 1): (start - 1 + limit)]
        return jsonify(obj) 
    elif request.method == "POST":
        data = request.get_json()
        pay_participant = data["payment"] / data["participants_number"]
        plan = Plan(
            name = data["name"],
            payment = data["payment"],
            card_number = data["card_number"],
            participants_number = data["participants_number"],
            status = data["status"],
            participants_pay = pay_participant,
            type_pay = data["type_pay"],
            owner_id = data["owner_id"],
        )
        db.session.add(plan)
        db.session.commit()
        return jsonify(plan.to_dict()), 201

@api.route("/plan/<int:id>/", methods=["GET", "PATCH"])
def plan(id):
    if request.method == "GET":
        plan = Plan.query.get(id)
        return jsonify({"plan": plan.to_dict()})
    elif request.method == "PATCH":
        plan = Plan.query.get(id)
        data = request.get_json()
        pay_participant = data["payment"] / data["participants_number"]
        plan.name = data["name"]
        plan.payment = data["payment"]
        plan.card_number = data["card_number"]
        plan.participants_number = data["participants_number"]
        plan.status = data["status"]
        plan.participants_pay = pay_participant
        plan.type_pay = data["type_pay"]
        plan.owner_id = data["owner_id"]
        db.session.commit()
        return jsonify(plan.to_dict())

@api.route("/plan/<int:id>/add_participants/", methods=["PATCH"])
def add_participants(id):
    plan = Plan.query.get(id)
    data = request.get_json()
    for user in data["id"]:
        user_id = User.query.get(user)
        plan.users.append(user_id)
    db.session.commit()
    return jsonify(plan.to_dict())
    
@api.route("/remove/participants/<int:participant_id>/plan/<int:plan_id>", methods=["PATCH"])
def remove_participants_plan(participant_id, plan_id):
    PlanUser.query.filter(PlanUser.plan_id==plan_id,PlanUser.user_id==participant_id).delete()
    db.session.commit()
    plan = Plan.query.get(plan_id)
    return jsonify({"plan": plan.to_dict()})

@api.route("/payments", methods=["GET", "POST"])
def fetch_pays():
    if request.method == "GET":
        payments = Payment.query.all()
        return jsonify({"payments": [p.to_dict() for p in payments]})
    
    elif request.method == "POST":
        data = request.get_json()
        if len(data["make_payment"]) > 1:
            for pay in data["make_payment"]:
                payment = Payment(
                    created_at = data["created_at"],
                    payment_month = pay,
                    participant_id = data["participant"],
                    plan_id = data["plan"],
                )
                db.session.add(payment)
                db.session.commit()
        else:
            payment = Payment(
                created_at = data["created_at"],
                payment_month = data["make_payment"],
                participant_id = data["participant"],
                plan_id = data["plan"],
            )

        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.to_dict()), 201

@api.route("/payments_by_plan/<int:id>", methods=["GET"])
def fetch_payments_by_plan(id):
    payments = Payment.query.filter(Payment.plan_id==id)
    return jsonify([p.to_dict() for p in payments], 201)
