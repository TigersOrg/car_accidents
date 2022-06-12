import datetime
from marshmallow import fields, Schema
from models.car_model import CarSchema
from models.init_db import bcrypt, db
from models.owner_car_model import owner_car


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    car_num = db.Column(db.String(20))
    country = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    a_role = db.Column(db.String(20), nullable=False)  # driver, worker
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=True)
    cars = db.relationship('Car', secondary=owner_car, lazy='subquery', backref=db.backref('users', lazy=True))

    def __init__(self, data):
        """
        Class constructor
        """

        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.phone = data.get('phone')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.car_num = data.get('car_num')
        self.country = data.get('country')
        self.city = data.get('city')
        self.a_role = data.get('a_role')
        self.created = datetime.datetime.utcnow()
        self.updated = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(value):
        return User.query.filter_by(email=value).first()

    # hash user's password before saving it into the db
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    # validate user's password during login
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: first_name='%s', email='%s'" % (self.first_name, self.email)


class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    car_num = fields.Str(required=True)
    country = fields.Str(required=True)
    city = fields.Str(required=True)
    a_role = fields.Str(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
    cars = fields.Nested(CarSchema, many=True)
