from flask import request, Blueprint, jsonify

from flask.views import MethodView
from models.car_model import Car, CarSchema
from utils.authentication import check_token, generate_token
from utils.custom_response import custom_response


# car_api = Blueprint('car_api', __name__)
car_schema = CarSchema()


class Cars(MethodView):
    """
    The class represents a group of endpoints dealing with cars
    """
    def post(self):
        """
        Create car
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

    def get(self, car_id=None):
        """
        Get cars
        """
        if car_id is None:
            cars = Car.get_all_cars()  # get all cars
            ser_data = car_schema.dump(cars, many=True)
            return custom_response(ser_data, 200)
        else:
            car = Car.get_one_car(car_id)  # get a certain car
            if not car:
                return custom_response({'error': 'car not found'}, 404)
            ser_data = car_schema.dump(car)
            return custom_response(ser_data, 200)

    def patch(self, car_id):

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

    def delete(self, car_id):

        """
        Delete a car
        """
        car = Car.get_one_car(car_id)
        if not car:
            return custom_response({'error': 'car not found'}, 404)
        car.delete()
        # return custom_response({'message': 'deleted'}, 204)
        return jsonify({'message': 'deleted'}, 204)
