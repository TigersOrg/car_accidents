import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from flask import request, jsonify, g
import os
from functools import wraps
from datetime import timedelta, datetime


# create jwt token
def generate_token(user_id):
    jwt_secret = os.environ.get('JWT_SECRET_KEY')
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=24),
        "id": user_id,
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return {'Authorization': token}


def check_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt_secret = os.environ.get('JWT_SECRET_KEY')

        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Authorization header missing"}, 401)

        auth_type, token = auth.split()
        if auth_type.lower() != "bearer":
            return jsonify({"error": "Invalid header. Authorization header must start with Bearer"}, 401)
        try:
            jwt.decode(
                token,
                jwt_secret,
                algorithms=["HS256"]
            )
            return f(*args, **kwargs)
        except (
                InvalidSignatureError,
                ExpiredSignatureError,
                DecodeError
        ):
            return jsonify({'error': 'invalid token'}), 401

    return wrapper
