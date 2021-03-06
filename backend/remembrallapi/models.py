"""
Data Classes for the remembrall application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return "%s(%s)" % (
            self.__class__.__name__,
            {column: value for column, value in self.to_dict().items()},
        )

    def json(self):
        """
        Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime(
                "%Y-%m-%d"
            )
            for column, value in self._to_dict().items()
        }


class PlanUser(db.Model):
    __tablename__ = "plans_users"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, ForeignKey("plans.id"))
    user_id = db.Column(db.Integer, ForeignKey("users.id"))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        if not email or not password:
            return None
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def to_dict(self):
        return dict(
            email=self.email,
        )

class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    date_on = db.Column(db.DateTime)
    payment = db.Column(db.Float)
    card_number = db.Column(db.Text)
    participants_number = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    participants_pay = db.Column(db.Numeric)
    type_pay = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, ForeignKey("users.id"))
    users = db.relationship("User", secondary="plans_users", backref="Plan")
    owner = db.relationship("User", backref="plans", lazy=False)
    # pays = db.relationship('Plan', backref='pay', lazy=False)

    def to_dict(self):
        return dict(
            name=self.name,
            date_on=self.date_on,
            payment=str(self.payment),
            card_number=self.card_number,
            participants_number=self.participants_number,
            status=self.status,
            participants_pay=str(self.participants_pay),
            type_pay=str(self.type_pay),
            owner_id=self.owner_id,
            users=[user.to_dict() for user in self.users],
            owner={"id": self.owner.id, "email": self.owner.email},
        )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_month = db.Column(db.Text)
    participant_id = db.Column(db.Integer, ForeignKey("users.id"))
    plan_id = db.Column(db.Integer, ForeignKey("plans.id"))
    participant = db.relationship("User", backref="user", lazy=False)
    plan = db.relationship("Plan", backref="plan", lazy=False)


    def to_dict(self):
        return dict(
            created_at=self.created_at,
            payment_month=self.payment_month,
            participant={"id": self.participant.id, "name": self.participant.email},
            plan={"id": self.plan.id, "name": self.plan.name},
        )
