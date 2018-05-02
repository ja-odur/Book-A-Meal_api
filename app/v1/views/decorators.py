from functools import wraps
from flask import request, make_response, jsonify
import jwt


def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return make_response(jsonify(dict(error='Token required')), 401)

        try:
            data = jwt.decode(token, 'SECRET_KEY_1738')
        except:
            pass



