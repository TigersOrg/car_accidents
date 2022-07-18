import datetime
import jwt
import os
import redis

from flask import Flask, jsonify, request
from models.init_db import bcrypt, db
from models.car_model import CarSchema
from models.user_model import UserSchema
from routes.car_routes import Cars
from routes.user_routes import Users
from routes.user_car_routes import UserCar
from utils.custom_response import custom_response
from domain.user_client import get_user_by_email_from_db

user_schema = UserSchema()
car_schema = CarSchema()

# todo: load dotenv to use .env
env_name = os.getenv('FLASK_ENV')

app = Flask(__name__)

app.config.from_object('config.Config')

# add rules for user view
user_view = Users.as_view('users')
app.add_url_rule('/api/v1/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/api/v1/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/api/v1/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])

# add rules for user_car view
user_car_view = UserCar.as_view('user_car')
app.add_url_rule('/api/v1/user_car/', view_func=user_car_view, methods=['GET'])
app.add_url_rule('/api/v1/user_car/<int:user_id>', view_func=user_car_view, methods=['POST'])
app.add_url_rule('/api/v1/user_car/<int:user_id>', view_func=user_car_view, methods=['PATCH'])

# add rules for cars view
car_view = Cars.as_view('cars')
app.add_url_rule('/api/v1/cars/', defaults={'car_id': None}, view_func=car_view, methods=['GET'])
app.add_url_rule('/api/v1/cars/', view_func=car_view, methods=['POST'])
app.add_url_rule('/api/v1/cars/<int:car_id>', view_func=car_view, methods=['GET', 'PATCH', 'DELETE'])

r = redis.Redis(host='redis', port=7777)

bcrypt.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()


# test first endpoint
@app.route('/')
def test_endpoint():
    return f'test endpoint works'

# test jwt
def make_set_jwt(jwt_type, user_login, uid):
    if not jwt_type in ['access', 'refresh']:
        raise TypeError

    JWT = jwt.encode(
        {
            "user": user_login,
            "uid": uid,
            # using that throws an ExpiredSignatureError
            # "exp": datetime.datetime.now() + datetime.timedelta(hours=1 if jwt_type == 'access' else 10)
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, os.environ.get('JWT_SECRET_KEY')
        # app.config['SECRET_KEY']
    )
    r.setex(f"{uid}:{jwt_type}", 60 if jwt_type == 'access' else 3600, JWT)

    return JWT


# test  login endpoint
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    # with engine.connect() as conn:
    #     data_response = conn.execute(f"SELECT email, password, uuid FROM Users WHERE email = '{email}'")
    #     uemail, upassword, uuid = data_response.first()

    user = get_user_by_email_from_db(email)
    uuid = user.id
    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)
    if not user.check_hash(password):
        return custom_response({'error': 'invalid credentials'}, 400)

    if r.exists(f"{uuid}:access") and r.ttl(f"{uuid}:access") > 1:
        # todo unify response
         return jsonify(
            {
                "token": r.get(f"{uuid}:access"),
                "refresh": r.get(f"{uuid}:refresh")
            }
         )

    if email is None:
        return f"response: user doesn't exist"
    else:
        if user.check_hash(password):
            access = make_set_jwt("access", email, uuid)
            refresh = make_set_jwt("refresh", email, uuid)

            # todo unify response
            jwtheaders = {}
            jwtheaders["Authorization"] = 'Bearer {}'.format(access)
            jwtheaders["RefreshAuth"] = refresh

            return {"Authorization": access, "RefreshAuth": refresh }, 200, jwtheaders
        else:
            return {"Error": "Incorrect password"}, 401


if __name__ == '__main__':
    app.run(debug=True)
