import unittest
import json

from run import app


class TestMeals(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='default22@gmail.com', username='default22', password='12345',
                             confirm_password='12345', address='address1', first_name='odur', last_name='joseph')
        self.reg_data_user = dict(category='user', email='agnes@gmail.com', username='agnes', password='12345',
                                  confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        self.login_data = dict(category='caterer', username='default22', password='12345')
        self.login_data_user = dict(category='user', username='agnes', password='12345')

        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_results = json.loads(self.response.data.decode())
        self.token = self.response_results['token']

    def test_create_meals(self):
        input_data = dict(name='meal', price=5000)
        expected_response_message = 'Meal {} successfully added.'.format(input_data['name'])
        token = self.token
        get_response = self.tester.post('api/v1/meals/', headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_meals(self):
        input_data = dict(name='meal', price=5000)
        token = self.token
        expected_response_message = [[1, 'meal', 5000, 1, 'default22'], [3, 'meal', 5000, 0, 'default22'],
                                     [4, 'meal', 5000, 0, 'default22'], [5, 'meal', 5000, 0, 'default22']]
        self.tester.post('api/v1/meals/', content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        get_response = self.tester.get('api/v1/meals/', headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal(self):
        token = self.token
        input_data = dict(name='meal', price=5000)
        update_data = dict(price=6000)
        expected_response_message = [3, 'meal', 6000, 0, 'default22']
        self.tester.post('api/v1/meals/', content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        get_response = self.tester.put('api/v1/meals/2', content_type="application/json",
                                       headers={'access-token':token}, data=json.dumps(update_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_meal(self):
        token = self.token
        input_data = dict(name='meal', price=5000)
        expected_response_message = [[1, 'meal', 5000, 0, 'default22'], [3, 'meal', 5000, 0, 'default22']]
        self.tester.post('api/v1/meals/', content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data),
                         headers={'access-token': token})
        self.tester.delete('api/v1/meals/2', headers={'access-token':token})
        get_response = self.tester.get('api/v1/meals/', headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_easy_point(self):
        token = self.token
        expected_results = 1

        response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                         data=json.dumps(self.login_data_user))
        response_results = json.loads(response.data.decode())
        token_user = response_results['token']

        self.tester.post('api/v1/meals/point/1', headers={'access-token': token_user})

        response = self.tester.get('api/v1/meals/', headers={'access-token': token})

        response_results = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected_results, response_results['message'][0][3])


if __name__ == '__main__':
    unittest.main()