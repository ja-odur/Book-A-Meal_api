from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.utils import sign_up, verify_registration_data, log_in
from app.v1.views.decorators import token_required
from app.v1.models.models import User, Caterer

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
        user_data = dict(category=data['category'], email=data['email'], username=data['username'],
                         first_name=data['first_name'], last_name=data['last_name'], password=data['password'],
                         confirm_password=data['confirm_password'], brand_name=data['brand_name'],
                         address=data['address'])
    except KeyError:
        return make_response(jsonify(dict(message='PROVIDE ALL REQUIRED INFORMATION.')), 400)

    error_response = verify_registration_data(user_data)

    if error_response:
        return make_response(jsonify({'message': error_response['message']}), error_response['status_code'])

    new_sign_up = sign_up(**user_data)

    return make_response(jsonify({'message': new_sign_up['message']}), new_sign_up['status_code'])


@users.route('/auth/login', methods=['POST'])
@swag_from('api_doc/user_login.yml')
def login():
    """
    This function logs in users
    :return: returns a token valid for 30 minutes
    """
    data = request.get_json()
    try:
        if data['category'] and data['username'] and data['password']:
            pass
    except KeyError:
        return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    new_login = log_in(category=data['category'], username=data['username'], password=data['password'])

    if new_login['operation']:
        return make_response(jsonify({'token': new_login['token']}), new_login['status_code'])
    return make_response(jsonify({'message': new_login['message']}), new_login['status_code'])


@users.route('/account', methods=['DELETE'])
@token_required()
def delete_account(current_user):
    category = current_user[0]
    username = current_user[1]

    if category == 'user':
        deleted = User.delete_user(username=username)
    else:
        deleted = Caterer.delete_caterer(username=username)

    if deleted:
        return make_response(jsonify({'message': 'Account successfully deleted'}), 200)
    # return make_response(jsonify({'message': 'Account deletion failed'}), 404






