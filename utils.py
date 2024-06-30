from functools import wraps
from flask import request, jsonify, make_response
from services.cache_service import app_cache

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not app_cache.is_user_logged_in(token):
            return make_response(jsonify({"message": "Login required"}), 401)
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not app_cache.is_user_manager(token):
            return make_response(jsonify({"message": "Permission not allowed"}), 401)
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not app_cache.is_user_customer(token):
            return make_response(jsonify({"message": "Permission not allowed"}), 401)
        return f(*args, **kwargs)
    return decorated_function
