
import jwt
import datetime
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

# def verify_input_data(category, email, username, first_name, Last_name, password, confirm_password, address):


def verify_input_data(**input_data):
    for data in input_data.values():
        if not data:
            return False

    at_char_found, at_count, period_count = False, 0, 0

    for char in input_data['email']:
        if char == '@':
            at_count += 1
            at_char_found = True

        if at_char_found and char == '.':
            period_count += 1
    print('@', at_count, '.', period_count)
    if at_count != 1:
        return False
    if period_count != 1:
        return False
    return True





