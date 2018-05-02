import unittest
import json

from run import app


class TestSuccesfulRegistration(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        # self.get_response = None


    def test_successful_user_registration(self):
        input_data = dict(category='user', email='default23@gmail.com', username='default23', password='12345',
                          confirm_password='12345', address='address1')
        expected_response_message = 'User {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_successful_caterer_registration(self):
        input_data = dict(category='caterer', email='default@gmail.com', username='default', password='12345',
                          confirm_password='12345', address='address1', brand_name='easy_caterer')
        expected_response_message = 'Caterer {} successfully signed up.'.format(input_data['username'])
        get_response = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_duplicate_user_sign_up(self):
        input_data = dict(category='user', email='default223@gmail.com', username='default3323', password='12345',
                          confirm_password='12345', address='address1')

        # initialsignup
        get_response1 = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(input_data))

        #second signup
        get_response3 = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response3.data.decode())
        print(response_results)

        expected_response_message = 'User {} already exists.'.format(input_data['username'])

        self.assertEqual(get_response3.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])


    def test_login_user(self):
        reg_data = dict(category='user', email='default@gmail.com', username='default', password='12345',
                        confirm_password='12345', address='address1')
        login_data = dict(category='user', username='default', password='12345')

        expected_response_message = 'user successfully logged in'
        register_user = self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(reg_data))

        get_response = self.tester.post('api/v1/auth/login', content_type="application/json", data=json.dumps(login_data))

        response_results = json.loads(get_response.data.decode())
        print(get_response.status_code)

        self.assertEqual(get_response.status_code, 401)
        self.assertEqual(expected_response_message, response_results['message'])

if __name__ == '__main__':
    unittest.main()