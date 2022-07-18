from flask import jsonify, request
from models.user_model import User, UserSchema

from utils.custom_response import custom_response
from utils.db_client import save, update, delete


user_schema = UserSchema()


def get_all_users_from_db():
    return User.query.all()


def get_one_user_from_db(id):
    return User.query.get(id)


def get_user_by_email_from_db(value):
    return User.query.filter_by(email=value).first()


# todo: query.get_or_404(id)
def get_all_users():
    users = get_all_users_from_db()
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)


def get_one_user(user_id):
    user = get_one_user_from_db(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


# todo:  select existed users
def create_user():
    req_data = request.get_json()
    # check if user already exists in the db
    user_in_db = get_user_by_email_from_db(req_data.get('email'))
    if user_in_db:
        return custom_response({'error': 'User already exist'}, 400)
    user = User(req_data)
    save(user)
    ser_data = user_schema.dump(user)
    return custom_response({'new user': ser_data}, 201)


def update_user(user_id):
    req_data = request.get_json()
    user = get_one_user_from_db(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    update(user, req_data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


def delete_user(user_id):
    user = get_one_user_from_db(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    delete(user)
    return jsonify({'message': 'deleted'}, 204)
