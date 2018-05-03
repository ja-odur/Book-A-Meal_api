from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
import jwt
import datetime

from app.v1.models.models import DbUsers, DbCaterers

SECRET_KEY ='secretKey4512yek'

user_db = DbUsers()
caterer_db = DbCaterers()

users = Blueprint('users', __name__, url_prefix='/api/v1')


@users.route('/auth/signup', methods=['POST'])
@swag_from('api_doc/user_registration.yml')
def register_user():
    data = request.get_json()
    try:
        if data['category'] and data['email'] and data['username'] \
                and data['password'] and data['confirm_password'] and data['address']:
            pass
    except:
        return make_response(jsonify({'message': 'Invalid data format'}), 403)

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

    return make_response(jsonify({'message': 'category can either be user or caterer.'}), 403)


@users.route('/auth/login', methods=['POST'])
@swag_from('api_doc/user_login.yml')
def login():
    data = request.get_json()
    try:
        if data['category'] and data['username']:
            pass
    except KeyError:
        return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    if data['category'] == 'user':
        user_info = user_db.get_user(data['username'])
        if user_info:
            user_password = user_info['password']
            if user_password == data['password']:
                category = 'user'
                email = user_info['email']
                username = user_info['username']
                token_string = str(category)+','+str(username)+','+str(email)
                token = jwt.encode({'info': token_string,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                        SECRET_KEY)
                return make_response(jsonify(dict(token=token.decode('UTF-8'))), 200)

            else:
                return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)

    elif data['category'] == 'caterer':
        caterer_info = caterer_db.get_user(data['username'])

        if caterer_info:
            user_password = caterer_info['password']
            if user_password == data['password']:
                category = 'caterer'
                email = caterer_info['email']
                username = caterer_info['username']
                token_string = str(category) + ',' + str(username) + ',' + str(email)
                token = jwt.encode({'info': token_string,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                   SECRET_KEY,algorithm='HS256')
                return make_response(jsonify(dict(token=token.decode('UTF-8'))), 200)

            else:
                return make_response(jsonify({'message': 'Invalid Username or Password'}), 201)

    return make_response(jsonify({'message': 'Invalid Username or Password'}), 401)
