from flask import current_app, jsonify, request
from models.car_model import Car, CarSchema
from models.user_model import User, UserSchema

from utils.authentication import check_token
from utils.custom_response import custom_response

from flask.views import MethodView


user_schema = UserSchema()
car_schema = CarSchema()


class Users(MethodView):
    """
    The class represents a group of endpoints dealing with users
    """

    decorators = [check_token]

    def get(self, user_id=None):
        """
        Get users
        """

        if user_id is None:  # get all users
            users = User.get_all_users()
            ser_users = user_schema.dump(users, many=True)

            return custom_response(ser_users, 200)

        else:
            user = User.get_one_user(user_id)  # get a certain user
            if not user:
                return custom_response({'error': 'user not found'}, 404)

            ser_user = user_schema.dump(user)

            return custom_response(ser_user, 200)

    def post(self):

        """
        create a user
        """

        req_data = request.get_json()

        # check if user already exists in the db
        user_in_db = User.get_user_by_email(req_data.get('email'))
        if user_in_db:
            message = {'error': 'User already exist'}

            return custom_response(message, 400)

        user = User(req_data)
        user.save()

        ser_data = user_schema.dump(user)
        return custom_response({'new user': ser_data}, 201)

    def patch(self, user_id):

        """
        Update an existing user
        """
        req_data = request.get_json()
        user = User.get_one_user(user_id)
        if not user:
            return custom_response({'error': 'user not found'}, 404)
        user.update(req_data)
        ser_user = user_schema.dump(user)

        return custom_response(ser_user, 200)

    def delete(self, user_id):
        """
         Delete an existing user
        """
        user = User.get_one_user(user_id)
        if not user:
            return custom_response({'error': 'user not found'}, 404)
        user.delete()

        return jsonify({'message': 'deleted'}, 204)  # todo: custom_response() doesn't work


class OwnerCar(MethodView):
    """
    The class represents a group of endpoints dealing with owner_user relation
    """

    def get(self):

        """
        get all users and their cars
        """
        users_list = []
        users = User.get_all_users()

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

            message = 'a list of users with there cars'

        return jsonify({message: users_list})

    def post(self, user_id):

        """
        Create a relation between a user and cars
        """

        req_data = request.get_json()
        # Get a user and associate with cars
        user = User.get_one_user(user_id)
        car_id_list = req_data['car_id']
        if user:
            cars = Car.query.filter(Car.id.in_(car_id_list)).all()
            user.cars = []  # Remove previous entry
            for car in cars:
                user.cars.append(car)
            user.save()
        message = "Data successfully Inserted"

        return jsonify({'message': message}, 400)

    def patch(self, user_id):

        """
        Update a relation between a user and cars
        """
        req_data = request.get_json()
        user = User.get_one_user(user_id)
        car_id_list = req_data['car_id']
        if user:
            cars = Car.query.filter(Car.id.in_(car_id_list)).all()
            user.cars = []  # Remove previous entry
            for car in cars:
                user.cars.append(car)
            user.save()
            message = 'Data has been updated'

        return jsonify({'message': message}, 400)
