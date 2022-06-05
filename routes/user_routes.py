from flask import  Blueprint, jsonify, request
from models.car_model import Car, CarSchema
from models.user_model import User, UserSchema

from utils.authentication import check_token, generate_token
from utils.custom_response import custom_response


user_api = Blueprint('users', __name__)
user_schema = UserSchema()
car_schema = CarSchema()


# Method POST http://127.0.0.1:5000/api/v1/users
@user_api.route('/', methods=['POST'])
def create():
    """
    Create a  user
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


# Method GET http://127.0.0.1:5000/api/v1/users
@user_api.route('/', methods=['GET'])
@check_token
def get_all():
    """
    Get all users
    """
    users = User.get_all_users()
    ser_users = user_schema.dump(users, many=True)

    return custom_response(ser_users, 200)


# Method GET http://127.0.0.1:5000/api/v1/users/<int:user_id>
@user_api.route('/<int:user_id>', methods=['GET'])
@check_token
def get_a_user(user_id):
    """
    Get a single user
    """
    user = User.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)

    return custom_response(ser_user, 200)


# Method PATCH http://127.0.0.1:5000/api/v1/users/<int:user_id>
@user_api.route('/<int:user_id>', methods=['PATCH'])
@check_token
def update(user_id):
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


# Method DELETE http://127.0.0.1:5000/api/v1/users/<int:user_id>
@user_api.route('/<int:user_id>', methods=['DELETE'])
@check_token
def delete(user_id):
    """
    Delete an existing user
    """
    user = User.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    user.delete()

    return jsonify({'message': 'deleted'}, 204)  # todo: custom_response() doesn't work


@user_api.route('/login', methods=['POST'])
def login():
    """
    User Login Function
    """
    req_data = request.get_json()
    if not req_data.get('email') or not req_data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)
    user = User.get_user_by_email(req_data.get('email'))
    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)
    if not user.check_hash(req_data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)
    ser_data = user_schema.dump(user)
    token = generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)


# Method POST http://127.0.0.1:5000/api/v1/users/create_user_car_relation/<int:user_id>
@user_api.route('/create_user_car_relation/<int:user_id>', methods=['POST'])
def user_car_create(user_id):
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
    # return message
    # ser_data = car_schema.dump(car)
    return jsonify({'message': message}, 400)


# Method PATCH http://127.0.0.1:5000/api/v1/users/update_user_car_relation/<int:user_id>
@user_api.route('/update_user_car_relation/<int:user_id>', methods=['PATCH'])
def user_car_update(user_id):
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


# Method GET http://127.0.0.1:5000/api/v1/users/get_all_users_with_cars
@user_api.route('/get_all_users_with_cars/', methods=['GET'])
def get_users_with_cars():
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
