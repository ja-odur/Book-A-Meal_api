from functools import wraps
from flask import request, make_response, jsonify
# from run import app
import jwt

# SECRET_KEY = app.config['API_KEY']
SECRET_KEY ='secretKey4512yek'


def token_required(admin=False):
    """
    This function is used to decorate routes inorder to include token authentication.
    :param admin: If set to True, the wrap function is only available to caterers
    :return:
    """
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
                    return make_response(jsonify(dict(message='Action not allowed for this user')), 401)

            return function(current_user, *args, **kwargs)

        return decorated

    return token_required_decorator






