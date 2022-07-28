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

    def __repr__(self):
        return "Car_number: car_num='%s'" % self.car_num


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
