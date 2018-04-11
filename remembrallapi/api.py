"""
Provides the API endpoints for consuming and producing
REST requests and responses
"""

from flask import Blueprint, jsonify, request
from remembrallapi.models import db, User, Plan, Pay, PlanUser

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET', 'POST'])
def fetch_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify({ 'users': [u.to_dict() for u in users] })
    elif request.method == 'POST':
        data = request.get_json()
        user = User(
            name=data['name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            avatar=data['avatar']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()),201

@api.route('/user/<int:id>/', methods=['GET'])
def user(id):
    user = User.query.get(id)
    return jsonify({ 'user': user.to_dict() })

@api.route('/plans', methods=['GET', 'POST'])
def fetch_plans():
    if request.method == 'GET':
        plans = Plan.query.all()
        return jsonify({ 'plans': [p.to_dict() for p in plans] })
