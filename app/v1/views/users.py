from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from env_config import API_KEY
import jwt
import datetime

from app.v1.models.users import DbUsers
from app.v1.models.caterers import DbCaterers

SECRET_KEY = API_KEY
# SECRET_KEY ='secretKey4512yek'

user_db = DbUsers()
caterer_db = DbCaterers(user_db)

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
        if data['category'] and data['email'] and data['username'] \
                and data['password'] and data['confirm_password'] and data['address']:
            pass
    except:
        return make_response(jsonify({'message': 'Invalid data format'}), 403)

    if data['password'] == data['confirm_password']:
        if data['category'] == 'user':
            add_user = user_db.add_user(email=data['email'], username=data['username'], password=data['password'],
                                        address=data['address'])

            if add_user:
                message = 'User {} successfully signed up.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 201)
            else:
                message = 'User {} already exists.'.format(data['username'])
                message.encode('utf-8')
                return make_response(jsonify(dict(message=message)), 403)

        elif data['category'] == 'caterer':
            add_caterer = caterer_db.add_caterer(email=data['email'], username=data['username'],
                                                 password=data['password'], address=data['address'])
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
        users_info = user_db.get_users()
        for user in users_info.values():
            if user['username'] == data['username']:
                user_info = user

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
                return make_response(jsonify({'message': 'Invalid Username or Password1'}), 401)
        else:
            return make_response(jsonify({'message': 'Invalid Username or Password2'}), 401)

    elif data['category'] == 'caterer':
        caterer_info = False
        caterer_ids = caterer_db.get_caterers().keys()
        for caterer_id in caterer_ids:
            info = caterer_db.get_caterer(caterer_id)
            if info['username'] == data['username']:
                caterer_info = info
                break

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
                return make_response(jsonify({'message': 'Invalid Username or Password1'}), 201)

    return make_response(jsonify({'message': 'Invalid Username or Password2'}), 401)
