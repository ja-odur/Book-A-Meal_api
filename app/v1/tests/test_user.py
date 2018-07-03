import unittest
import json

from run import app
from app.v1.models.db_connection import DB

URL_PREFIX = 'api/v1'


class TestSuccessfulRegistration(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        self.signup_url = URL_PREFIX + '/auth/signup'
        self.login_url = URL_PREFIX + '/auth/login'

        self.tester = app.test_client(self)

    def tearDown(self):
        DB.drop_all()

    def test_successful_user_registration(self):
        input_data = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                          confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        expected_response_message = 'User {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(201, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_successful_caterer_registration(self):
        input_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'Caterer {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(201, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_duplicate_user_sign_up(self):
        input_data = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                          confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        # initial signup
        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(input_data))

        # second signup
        get_response3 = self.tester.post(self.signup_url, content_type="application/json",
                                         data=json.dumps(input_data))

        response_results = json.loads(get_response3.data.decode())

        expected_response_message = 'User {} already exists.'.format(input_data['username'])

        self.assertEqual(403, get_response3.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_login_user(self):
        reg_data = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                        confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        login_data = dict(category='user', username='user1', password='12345')

        self.tester.post( self.signup_url, content_type="application/json", data=json.dumps(reg_data))

        get_response = self.tester.post(self.login_url, content_type="application/json",
                                        data=json.dumps(login_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertIn('token', response_results)

    def test_empty_data_submission(self):
        input_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='')
        expected_response_message = 'Invalid data format. Check email field and fill in all fields.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_required_data_missing(self):
        input_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur')
        expected_response_message = 'PROVIDE ALL REQUIRED INFORMATION.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_double_at_in_email(self):
        input_data = dict(category='caterer', email='caterer1@@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'Invalid data format. Check email field and fill in all fields.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_invalid_category(self):
        input_data = dict(category='invalid_category', email='caterer1@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'category can either be user or caterer.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_signup_password_dont_match(self):
        input_data = dict(category='invalid_category', email='caterer1@gmail.com', username='caterer1', password='12345',
                          confirm_password='12345678', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'Passwords don\'t match.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_invalid_email(self):
        input_data = dict(category='caterer', email='caterer1@gmail..com', username='caterer1', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'Invalid data format. Check email field and fill in all fields.'
        get_response = self.tester.post(self.signup_url, content_type="application/json",
                                        data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_login_invalid_password(self):
        reg_data = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                        confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        login_data = dict(category='user', username='user1', password='123455678')

        self.tester.post( self.signup_url, content_type="application/json", data=json.dumps(reg_data))

        get_response = self.tester.post(self.login_url, content_type="application/json",
                                        data=json.dumps(login_data))

        self.assertEqual(401, get_response.status_code)

    def test_login_missing_required_data(self):
        reg_data = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                        confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        login_data = dict(username='user1', password='12345')

        self.tester.post( self.signup_url, content_type="application/json", data=json.dumps(reg_data))

        get_response = self.tester.post(self.login_url, content_type="application/json",
                                        data=json.dumps(login_data))

        self.assertEqual(401, get_response.status_code)


# if __name__ == '__main__':
#     unittest.main()