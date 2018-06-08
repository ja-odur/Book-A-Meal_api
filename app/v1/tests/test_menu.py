import unittest
import json

from run import app


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='default22@gmail.com', username='default22', password='12345',
                             confirm_password='12345', address='address1')
        self.login_data = dict(category='caterer', username='default22', password='12345')
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data))
        self.response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_results = json.loads(self.response.data.decode())
        self.token = self.response_results['token']

    def test_create_menu_successful(self):
        token = self.token
        menu = [[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]]
        input_data = dict(menu=menu)
        expected_response_message = 'Menu {} successfully added.'.format(menu)
        get_response = self.tester.post('api/v1/menu/', headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_menu_failure(self):
        token = self.token
        menu = dict(menu=[[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]])
        input_data = dict(menu=menu)
        expected_response_message = 'Bad data format'
        get_response = self.tester.post('api/v1/menu/', headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_menu(self):
        token = self.token
        menu = [[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]]
        return_dict = dict(default22=menu)
        expected_response_message = 'Todays menu {}.'.format(return_dict)
        get_response = self.tester.get('api/v1/menu/', headers={'access-token':token})

        print(get_response)
        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(expected_response_message, response_results['message'])


if __name__ == '__main__':
    unittest.main()
