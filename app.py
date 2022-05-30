import os

from flask import Flask
from config import app_config
from routes.user_routes import user_api as user_blueprint
from routes.car_routes import car_api as car_blueprint

from models.init_db import bcrypt, db


env_name = os.getenv('FLASK_ENV')

app = Flask(__name__)

app.config.from_object(app_config[env_name])
app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(car_blueprint, url_prefix='/api/v1/cars')

bcrypt.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def test_endpoint():
    return f'test endpoint works'


if __name__ == '__main__':
    app.run(debug=True)
