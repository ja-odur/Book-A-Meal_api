
import jwt
import datetime
from flask import jsonify, make_response
from env_config import API_KEY

SECRET_KEY = API_KEY
# SECRET_KEY ='secretKey4512yek'


def verify_password(username, user_email, db_password, input_password, category):
    if db_password == input_password:
        token_string = str(category) + ',' + str(username) + ',' + str(user_email)
        token = jwt.encode({'info': token_string,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           SECRET_KEY)
        return token.decode('UTF-8')
    return False

# def nm():
#     if data['category'] == 'user':
#         user_info = False
#         users_info = User.get_users()
#         for user in users_info:
#             if user.username == data['username']:
#                 user_info = user
#
#         if user_info:
#             token = verify_password(username=user_info.username, user_email=user_info.email, db_password=user_info.password,
#                                     input_password=data['password'], category='user')
#             if token:
#                 return make_response(jsonify(dict(token=token)), 200)
#
#             else:
#                 return make_response(jsonify({'message': 'Invalid Username or Password1'}), 401)
#         else:
#             return make_response(jsonify({'message': 'Invalid Username or Password2'}), 401)