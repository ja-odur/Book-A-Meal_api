from functools import wraps
from flask import request, make_response, jsonify
import jwt

SECRET_KEY ='secretKey4512yek'


def token_required(admin=False):
    def token_required_decorator(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            token = None

            if 'access-token' in request.headers:
                token = request.headers['access-token']

            if not token:
                return make_response(jsonify(dict(message='Token required')), 401)

            try:
                raw_data = jwt.decode(token, SECRET_KEY)
            except:
                return make_response(jsonify(dict(message='Token is invalid ')), 401)
            else:
                current_user = raw_data['info'].split(',')

            if admin:
                if current_user[0] != 'caterer':
                    return make_response(jsonify(dict(message='Action not allowed this user')), 401)

            return function(current_user, *args, **kwargs)

        return decorated

    return token_required_decorator






