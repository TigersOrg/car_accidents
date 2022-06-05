from models.init_db import db

# the mapping between User and Car
owner_car = db.Table('owner_car',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('car_id', db.Integer, db.ForeignKey('cars.id'))
                     )
