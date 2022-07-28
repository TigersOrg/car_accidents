from flask import request
from models.car_model import Car, CarSchema
from models.user_model import User, UserSchema

from utils.custom_response import custom_response
from utils.db_client import save


car_schema = CarSchema()
user_schema = UserSchema()


def get_all_users_from_db():
    return User.query.all()


def get_one_user_from_db(id):
    return User.query.get(id)


def get_users_and_cars():
    users_list = []
    users = get_all_users_from_db()
    for user in users:
        user_dict = {
            'name': user.first_name,
            'email': user.email
        }
        cars_list = []
        if user.cars:
            for car in user.cars:
                car_dict = {
                    'mark': car.mark,
                    'model': car.model,
                    'car number': car.car_num
                }
                cars_list.append(car_dict)
        user_dict.update({
            'cars': cars_list
        })
        users_list.append(user_dict)
    return custom_response({'List of users with there cars': users_list}, 200)


def create_relation_user_cars(user_id):
    req_data = request.get_json()
    # Get a user and their cars
    user = get_one_user_from_db(user_id)
    car_id_list = req_data['car_id']
    if user:
        cars = Car.query.filter(Car.id.in_(car_id_list)).all()
        user.cars = []  # Remove previous entry
        for car in cars:
            user.cars.append(car)
        save(user)
    return custom_response('Data successfully Inserted', 400)
