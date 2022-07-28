from flask import jsonify, request
from models.car_model import Car, CarSchema

from utils.custom_response import custom_response
from utils.db_client import save, update, delete


car_schema = CarSchema()


def get_all_cars_from_db():
    return Car.query.all()


def get_one_car_from_db(id):
    return Car.query.get(id)


def get_a_car_by_num_from_db(value):
    return Car.query.filter_by(car_num=value).first()


def get_all_cars_for_a_user(id):
    return Car.query.filter(Car.users.any(id=id)).all()


def create_car():
    req_data = request.get_json()
    car_in_db = get_a_car_by_num_from_db(req_data.get('car_num'))
    if car_in_db:
        return custom_response({'error': 'Car already exist'}, 400)
    car = Car(req_data)
    save(car)
    ser_data = car_schema.dump(car)
    return custom_response({'new car': ser_data}, 201)


def get_cars():
    cars = get_all_cars_from_db()
    ser_data = car_schema.dump(cars, many=True)
    return custom_response(ser_data, 200)


def get_one_car(car_id):
    car = get_one_car_from_db(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    ser_data = car_schema.dump(car)
    return custom_response(ser_data, 200)


def update_car(car_id):
    req_data = request.get_json()
    car = get_one_car_from_db(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    update(car, req_data)
    ser_data = car_schema.dump(car)
    return custom_response(ser_data, 200)


# todo: missing 1 required positional argument: 'car_id'
def delete_car(car_id):
    car = get_one_car_from_db(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    delete(car)
    return jsonify({'message': 'deleted'}, 204)
