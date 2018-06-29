import unittest
import json

from run import app
from app.v1.models.db_connection import DB

URL_PREFIX = 'api/v1'


class TestMeals(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        signup_url = URL_PREFIX + '/auth/signup'
        login_url = URL_PREFIX + '/auth/login'
        self.meals_url = URL_PREFIX + '/meals/'

        self.tester = app.test_client(self)

        self.reg_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                             confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        self.reg_data_user = dict(category='user', email='agnes@gmail.com', username='agnes', password='12345',
                                  confirm_password='12345', address='address1', first_name='agnes', last_name='a')

        self.login_data = dict(category='caterer', username='caterer1', password='12345')
        self.login_data_user = dict(category='user', username='agnes', password='12345')

        self.tester.post(signup_url, content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post(signup_url, content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response = self.tester.post(login_url, content_type="application/json",
                                         data=json.dumps(self.login_data))

        self.response_results = json.loads(self.response.data.decode())
        self.token = self.response_results['token']

    def tearDown(self):
        DB.drop_all()

    def test_create_meals(self):
        input_data = dict(name='meal', price=5000)
        expected_response_message = 'Meal {} successfully added.'.format(input_data['name'])
        token = self.token
        get_response = self.tester.post(self.meals_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_meals(self):
        input_data = dict(name='meal', price=5000)
        token = self.token
        expected_response_message = [{'caterer': 1, 'meal_id': 1, 'name': 'meal', 'point': 0, 'price': 5000}]
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))

        get_response = self.tester.get(self.meals_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal(self):
        token = self.token

        input_data = dict(name='meal', price=5000)
        update_data = dict(price=6000)
        update_id = '1'
        update_url = self.meals_url + update_id

        expected_response_message = [{'caterer': 1, 'meal_id': 1, 'name': 'meal', 'point': 0, 'price': 6000}]

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.put(update_url, content_type="application/json",
                        headers={'access-token':token}, data=json.dumps(update_data))

        get_response = self.tester.get(self.meals_url, headers={'access-token': token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_meal(self):
        token = self.token
        delete_id = '1'
        delete_url = self.meals_url + delete_id
        input_data = dict(name='meal', price=5000)
        expected_response_message = [{'caterer': 1, 'meal_id': 2, 'name': 'meal', 'point': 0, 'price': 5000}]
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.post(self.meals_url, content_type="application/json", data=json.dumps(input_data),
                         headers={'access-token': token})
        self.tester.delete(delete_url, headers={'access-token':token})
        get_response = self.tester.get(self.meals_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_easy_point(self):
        token = self.token
        expected_results = 1
        point_id = '1'
        point_url = URL_PREFIX + '/meals/point/' + point_id

        input_data = dict(name='meal', price=5000)
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': token},
                         data=json.dumps(input_data))

        response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                    data=json.dumps(self.login_data_user))

        response_results = json.loads(response.data.decode())
        token_user = response_results['token']

        self.tester.post(point_url, headers={'access-token': token_user})

        response = self.tester.get(self.meals_url, headers={'access-token': token})

        response_results = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(expected_results, response_results['message'][0]['point'])


if __name__ == '__main__':
    unittest.main()