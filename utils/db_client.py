import datetime
from models.user_model import User

from models.init_db import db


def save(obj):
    db.session.add(obj)
    db.session.commit()


def update(obj, data):
    for key, value in data.items():
        if key == 'password':
            value = User.generate_hash(obj, value)
        setattr(obj, key, value)
    obj.updated = datetime.datetime.utcnow()
    db.session.commit()


def delete(obj):
    db.session.delete(obj)
    db.session.commit()
