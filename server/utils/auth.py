from functools import wraps

import jwt
from flask import request, jsonify

import config
from utils.time import delta, utcnow

JWT_ALGORITHM = 'HS256'


def generate_jwt_token(payload, exp_hours=1):
    if payload is None:
        payload = {}
    payload['exp'] = utcnow() + delta(hours=exp_hours)
    return jwt.encode(payload, config.SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token):
    """ decode jwt token and verify """
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def auth_required(*roles):
    """ Protects routes, requiring a JWT token and role verification """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                return jsonify({"error": "Token is missing!"}), 401

            token = token.split(" ")[1]  # Extract token after Bearer
            decoded = decode_jwt_token(token)

            if not decoded:
                return jsonify({"error": "Token is invalid or expired!"}), 401

            user_role = decoded.get("role_name")
            if roles and user_role not in roles:
                return jsonify({"error": "Permission denied!"}), 403

            request.auth_user = decoded
            return f(*args, **kwargs)  # Pass decoded user data

        return decorated_function

    return decorator
