"""
Data Classes for the remembrall application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

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
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    avatar = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            avatar=self.avatar,
            created_at=self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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
        print(self.owner.name)
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
            owner={"id": self.owner.id, "name": self.owner.name},
        )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    make_payments = db.Column(db.Boolean)
    number_pays = db.Column(db.Integer)
    payment_to = db.Column(db.DateTime)
    participant_id = db.Column(db.Integer, ForeignKey("users.id"))
    plan_id = db.Column(db.Integer, ForeignKey("plans.id"))

    def to_dict(self):
        return dict(
            make_payments=self.make_payments,
            number_payments=self.number_payments,
            payment_to=self.payment_to,
            participant=self.participant_id,
            plan=self.plan_id,
        )
