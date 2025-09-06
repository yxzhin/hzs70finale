import jwt
from datetime import datetime, timezone, timedelta
from server.app.conf import Config
from functools import wraps
from flask import request


def encode_token(user_id: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    payload = {
        'user_id': user_id,
        'exp': expiration,
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        print("JWT Error: Signature has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"JWT Error: Invalid token. {e}")
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return {"message": "Token is missing"}, 401

        user_id = decode_token(token)
        if not user_id:
            return {"message": "Invalid or expired token"}, 401

        return f(user_id=user_id, *args, **kwargs)

    return decorated
