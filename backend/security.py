import datetime as dt
import jwt
from functools import wraps
from flask import request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import SECRET_KEY

TOKEN_HOURS = 8

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

def create_token(user_id: int) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + dt.timedelta(hours=TOKEN_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user_id():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_current_user_id()
        if user_id is None:
            return jsonify({"error": "Authentication required"}), 401
        g.user_id = user_id
        return fn(*args, **kwargs)
    return wrapper
