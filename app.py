import datetime
import jwt
import os
import redis

from flask import Flask, jsonify, request

from config import app_config
from models.init_db import bcrypt, db
from models.car_model import Car, CarSchema
from models.user_model import User, UserSchema
from routes.car_routes import car_api as car_blueprint
from routes.user_routes import user_api as user_blueprint
from utils.custom_response import custom_response


user_schema = UserSchema()
car_schema = CarSchema()

env_name = os.getenv('FLASK_ENV')

app = Flask(__name__)

app.config.from_object(app_config[env_name])
app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(car_blueprint, url_prefix='/api/v1/cars')

r = redis.Redis(host='localhost', port=6379)

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

    user = User.get_user_by_email(email)
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


# # add some sample data into database
# @app.route('/init-sample-data')
# def init_sample_data():
#     owner_and_car_list = []
#     for user_number in range(3):
#         user = User(
#             first_name="User " + str(user_number),
#             last_name="LastName " + str(user_number),
#             phone="777-87-97" + str(user_number),
#             email="user-" + str(user_number) + "@email.com",
#             password='password' + str(user_number),
#             car_num='AE5678' + str(user_number) + 'KY',
#             country='Ukraine',
#             city='Dnipro',
#             role='worker')
#
#         owner_and_car_list.append(user)
#
#     for car_number in range(5):
#         car = Car(mark="Kia", model="Sportage", car_num='AE5678' + str(car_number) + 'KY')
#         owner_and_car_list.append(car)
#
#     db.session.add_all(owner_and_car_list)
#     db.session.commit()
#     return "Successfully Initialized"


if __name__ == '__main__':
    app.run(debug=True)
