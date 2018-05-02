from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from

from app_v1.models.models import DbUsers, DbCaterers

user_db = DbUsers()
caterer_db = DbCaterers()

users = Blueprint('users', __name__, url_prefix='/api/v1')


@users.route('/auth/signup', methods=['POST'])
@swag_from('api_doc/user_registration.yml')
def register_user():
    data = request.get_json()
    if data['password'] == data['confirm_password']:
        if data['category'] == 'user':
            add_user = user_db.add_user(data['email'], data['username'], data['password'], data['address'])

            if add_user:
                message = 'User {} successfully signed up.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 201)
            else:
                message = 'User {} already exists.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 403)

        elif data['category'] == 'caterer':
            add_caterer = caterer_db.add_user(data['email'], data['username'], data['password'], data['address'],
                                brand_name='easy_brand')
            if add_caterer:
                message = 'Caterer {} successfully signed up.'.format(data['username'])
                return make_response(jsonify(dict(message=message)), 201)
            else:
                message = 'Caterer {} already exists.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 403)


@users.route('/auth/login', methods=['POST'])
@swag_from('api_doc/user_login.yml')
def login():
    data = request.get_json()
    if data['category'] == 'user':
        user_info = user_db.get_user(data['username'])
        if user_info:
            user_password = user_info['password']
            if user_password == data['password']:
                return make_response(jsonify({'message':'user successfully logged in'}), 401)
            else:
                return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    elif data['category'] == 'caterer':
        caterer_info = caterer_db.get_user(data['username'])

        if caterer_info:
            user_password = caterer_info['password']
            if user_password == data['password']:
                return make_response(jsonify({'message': 'user successfully logged in'}), 401)
            else:
                return make_response(jsonify({'message': 'Invalid Username or Password'}), 201)
        else:
            return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)
