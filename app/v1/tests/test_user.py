import unittest
import json

from run import app
from app.v1.models.models import User, Caterer


class TestSuccessfulRegistration(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_successful_user_registration(self):
        input_data = dict(category='user', email='default233@gmail.com', username='default233', password='12345',
                          confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        expected_response_message = 'User {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post('api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps(input_data))
        # deleting user for recurrence purpose
        User.delete_user('default233')

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_successful_caterer_registration(self):
        input_data = dict(category='caterer', email='default100@gmail.com', username='default100', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer', first_name='odur',
                          last_name='joseph')
        expected_response_message = 'Caterer {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post('api/v1/auth/signup', content_type="application/json",
                                        data=json.dumps(input_data))
        # deleting caterer for recurrence purpose
        Caterer.delete_caterer('default100')

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_duplicate_user_sign_up(self):
        input_data = dict(category='user', email='default223@gmail.com', username='default3323', password='12345',
                          confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        # initial signup
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(input_data))

        # second signup
        get_response3 = self.tester.post('api/v1/auth/signup', content_type="application/json",
                                         data=json.dumps(input_data))

        response_results = json.loads(get_response3.data.decode())

        expected_response_message = 'User {} already exists.'.format(input_data['username'])

        self.assertEqual(get_response3.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_login_user(self):
        reg_data = dict(category='user', email='default78@gmail.com', username='default78', password='12345',
                        confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        login_data = dict(category='user', username='default78', password='12345')

        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(reg_data))

        get_response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                        data=json.dumps(login_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 200)
        self.assertIn('token', response_results)


if __name__ == '__main__':
    unittest.main()