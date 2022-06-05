import datetime

from marshmallow import fields, Schema
from models.init_db import db


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    car_num = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=True)

    def __init__(self, data):
        """
        Class constructor
        """

        self.mark = data.get('mark')
        self.model = data.get('model')
        self.car_num = data.get('car_num')
        self.created = datetime.datetime.utcnow()
        self.updated = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_cars():
        return Car.query.all()

    @staticmethod
    def get_one_car(id):
        return Car.query.get(id)

    @staticmethod
    def get_all_cars_for_a_user(id):
        return Car.query.filter(Car.users.any(id=id)).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class CarSchema(Schema):
    """
    Car Schema
    """
    id = fields.Int(dump_only=True)
    mark = fields.Str(required=True)
    model = fields.Str(required=True)
    car_num = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
