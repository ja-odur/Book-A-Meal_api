from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.utils import verify_password, verify_input_data, verify_registration_data

from app.v1.models.models import User, Caterer

import jwt
import datetime
from env_config import API_KEY

SECRET_KEY = API_KEY


users = Blueprint('users', __name__, url_prefix='/api/v1')


@users.route('/auth/signup', methods=['POST'])
@swag_from('api_doc/user_registration.yml')
def register_user():
    """
    This function enables new users to signup. ensures that the usernames and email fields are unique in the database
    :return: returns a confirmation message
    """

    data = request.get_json()
    try:
        if data['category'] and data['email'] and data['username'] and data['first_name'] and data['last_name'] \
                and data['password'] and data['confirm_password'] and data['address']:
            pass
    except KeyError:
        pass

    error_response = verify_registration_data(category=data['category'], email=data['email'], username=data['username'],
                                        first_name=data['first_name'], last_name=data['last_name'],
                                        password=data['password'], confirm_password=data['confirm_password'],
                                        address=data['address'])

    if error_response:
        return make_response(jsonify({'message': error_response['message']}), error_response['status_code'])

    if data['password'] == data['confirm_password']:
        if data['category'] == 'user':
            new_user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
                            username=data['username'], password=data['password'], address=data['address']).add_user()

            if new_user:
                message = 'User {} successfully signed up.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 201)
            else:
                message = 'User {} already exists.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 403)

        elif data['category'] == 'caterer':
            new_caterer = Caterer(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
                            username=data['username'], password=data['password'], address=data['address']).add_caterer()
            if new_caterer:
                message = 'Caterer {} successfully signed up.'.format(data['username'])
                return make_response(jsonify(dict(message=message)), 201)
            else:
                message = 'Caterer {} already exists.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 403)

    return make_response(jsonify({'message': 'category can either be user or caterer.'}), 403)


@users.route('/auth/login', methods=['POST'])
@swag_from('api_doc/user_login.yml')
def login():
    """
    This function logs in users
    :return: returns a token valid for 30 minutes
    """
    data = request.get_json()
    try:
        if data['category'] and data['username']:
            pass
    except KeyError:
        return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    if data['category'] == 'user':
        user_info = False
        users_info = User.get_users()
        for user in users_info:
            if user.username == data['username']:
                user_info = user
                break

        if user_info:
            token = verify_password(username=user_info.username, user_email=user_info.email, db_password=user_info.password,
                                    input_password=data['password'], category='user')
            if token:
                return make_response(jsonify(dict(token=token)), 200)

        else:
            return make_response(jsonify({'message': 'Invalid Username or Password2'}), 401)

    elif data['category'] == 'caterer':
        caterer_info = False
        caterers_info = Caterer.get_caterers()
        for caterer in caterers_info:
            if caterer.username == data['username']:
                caterer_info = caterer
                break

        if caterer_info:
            token = verify_password(username=caterer_info.username, user_email=caterer_info.email,
                                    db_password=caterer_info.password,
                                    input_password=data['password'], category='caterer')
            if token:
                return make_response(jsonify(dict(token=token)), 200)

    return make_response(jsonify({'message': 'Invalid Username or Password2'}), 401)
