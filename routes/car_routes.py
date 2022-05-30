from flask import request, Blueprint, jsonify
from models.car_model import Car, CarSchema

from utils.authentication import check_token, generate_token
from utils.custom_response import custom_response


car_api = Blueprint('car_api', __name__)
car_schema = CarSchema()


# Method POST http://127.0.0.1:5000/api/v1/cars/
@car_api.route('/', methods=['POST'])
def create():
    """
    Create car 'function'
    """
    req_data = request.get_json()

    # todo: check if a car already exists in the db
    # car_in_db = Car.get_user_by_num(req_data.get('car_num'))
    # if car_in_db:
    #     message = {'error': 'Car already exists'}
    #     return custom_response(message, 400)

    car = Car(req_data)
    car.save()

    ser_data = car_schema.dump(car)
    return custom_response({'new car': ser_data}, 201)


# Method GET http://127.0.0.1:5000/api/v1/cars/
@car_api.route('/', methods=['GET'])
def get_all():
    """
    Get all cars
    """
    cars = Car.get_all_cars()
    ser_data = car_schema.dump(cars, many=True)
    return custom_response(ser_data, 200)


# Method GET http://127.0.0.1:5000/api/v1/cars/id
@car_api.route('/<int:car_id>', methods=['GET'])
def get_one(car_id):
    """
    Get a car
    """
    car = Car.get_one_car(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    ser_data = car_schema.dump(car)
    return custom_response(ser_data, 200)


# Method PATCH http://127.0.0.1:5000/api/v1/cars/id
@car_api.route('/<int:car_id>', methods=['PATCH'])
def update(car_id):
    """
    Update a car
    """
    req_data = request.get_json()
    car = Car.get_one_car(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    car.update(req_data)
    ser_data = car_schema.dump(car)
    return custom_response(ser_data, 200)


# Method DELETE http://127.0.0.1:5000/api/v1/cars/id
@car_api.route('/<int:car_id>', methods=['DELETE'])
def delete(car_id):
    """
    Delete a car
    """
    car = Car.get_one_car(car_id)
    if not car:
        return custom_response({'error': 'car not found'}, 404)
    car.delete()
    # return custom_response({'message': 'deleted'}, 204)
    return jsonify({'message': 'deleted'}, 204)