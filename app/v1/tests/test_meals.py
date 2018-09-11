import unittest
import json

from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB

URL_PREFIX = 'api/v1'


class TestMeals(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        self.signup_url = URL_PREFIX + '/auth/signup'
        self.login_url = URL_PREFIX + '/auth/login'
        self.meals_url = URL_PREFIX + '/meals/'

        self.tester = app.test_client(self)

        self.reg_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                             confirm_password='12345', address='address1', brand_name='easy_caterer',
                             first_name='odur', last_name='joseph')

        self.reg_data_user = dict(category='user', email='agnes@gmail.com', username='agnes', password='12345',
                                  confirm_password='12345', address='address1', brand_name='easy_caterer',
                                  first_name='agnes', last_name='a')

        self.login_data = dict(category='caterer', username='caterer1', password='12345')
        self.login_data_user = dict(category='user', username='agnes', password='12345')

        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response = self.tester.post(self.login_url, content_type="application/json",
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

        self.assertEqual(201, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_meals(self):
        input_data = dict(name='meal', price=5000)
        token = self.token
        expected_response_message = [{'caterer': 'easy_caterer', 'caterer_id': 1, 'meal_id': 1, 'name': 'meal',
                                      'point': 0, 'price': 5000}]
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))

        get_response = self.tester.get(self.meals_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal_price(self):

        input_data = dict(name='meal', price=5000)
        update_data = dict(price=6000)
        update_id = '1'
        update_url = self.meals_url + update_id

        expected_response_message = [{'caterer': 'easy_caterer', 'caterer_id': 1, 'meal_id': 1, 'name': 'meal',
                                      'point': 0, 'price': 6000}]

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':self.token},
                         data=json.dumps(input_data))
        self.tester.put(update_url, content_type="application/json",
                        headers={'access-token':self.token}, data=json.dumps(update_data))

        get_response = self.tester.get(self.meals_url, headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal_Name(self):
        token = self.token

        input_data = dict(name='meal', price=5000)
        update_data = dict(name='meal_updated')
        update_id = '1'
        update_url = self.meals_url + update_id

        expected_response_message = [{'caterer': 'easy_caterer', 'caterer_id': 1, 'meal_id': 1, 'name': 'meal_updated',
                                      'point': 0, 'price': 5000}]

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        self.tester.put(update_url, content_type="application/json",
                        headers={'access-token':token}, data=json.dumps(update_data))

        get_response = self.tester.get(self.meals_url, headers={'access-token': token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_meal(self):
        token = self.token
        delete_id = '1'
        delete_url = self.meals_url + delete_id
        input_data1 = dict(name='meal1', price=5000)
        input_data2 = dict(name='meal', price=5000)
        expected_response_message = [{'caterer': 'easy_caterer', 'caterer_id': 1, 'meal_id': 2, 'name': 'meal',
                                      'point': 0, 'price': 5000}]
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data1))
        self.tester.post(self.meals_url, content_type="application/json", data=json.dumps(input_data2),
                         headers={'access-token': token})
        self.tester.delete(delete_url, headers={'access-token':token})
        get_response = self.tester.get(self.meals_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_meal_failure(self):
        token = self.token
        delete_id = '4'
        delete_url = self.meals_url + delete_id
        input_data1 = dict(name='meal1', price=5000)
        input_data2 = dict(name='meal', price=5000)
        expected_response_message = 'Deletion failed, no item found to delete.'
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data1))
        self.tester.post(self.meals_url, content_type="application/json", data=json.dumps(input_data2),
                         headers={'access-token': token})
        get_response = self.tester.delete(delete_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_easy_point(self):
        token = self.token
        expected_results = 1
        point_id = '1'
        point_url = URL_PREFIX + '/meals/point/' + point_id

        input_data = dict(name='meal', price=5000)
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': token},
                         data=json.dumps(input_data))

        response = self.tester.post(self.login_url, content_type="application/json",
                                    data=json.dumps(self.login_data_user))

        response_results = json.loads(response.data.decode())
        token_user = response_results['token']

        self.tester.post(point_url, headers={'access-token': token_user})

        response = self.tester.get(self.meals_url, headers={'access-token': token})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_results, response_results['message'][0]['point'])

    def test_easy_point_failure(self):
        expected_results = 'Point out failed.'
        point_id = '5'
        point_url = URL_PREFIX + '/meals/point/' + point_id

        response = self.tester.post(self.login_url, content_type="application/json",
                                    data=json.dumps(self.login_data_user))

        response_results = json.loads(response.data.decode())
        token_user = response_results['token']

        response = self.tester.post(point_url, headers={'access-token': token_user})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_results, response_results['message'])

    def test_easy_point_caterer(self):
        expected_results = 'Operation not permitted for caterers.'
        point_id = '5'
        point_url = URL_PREFIX + '/meals/point/' + point_id

        response = self.tester.post(point_url, headers={'access-token': self.token})

        response_results = json.loads(response.data.decode())

        self.assertEqual(403, response.status_code)
        self.assertEqual(expected_results, response_results['message'])

    def test_create_meal_failure(self):
        input_data = dict(name1='meal', price=5000)
        expected_response_message = 'Invalid format.'
        token = self.token
        get_response = self.tester.post(self.meals_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_duplicate_meal_creation(self):
        input_data = dict(name='meal', price=5000)
        expected_response_message = 'Meal already exists.'
        token = self.token

        self.tester.post(self.meals_url, headers={'access-token': token}, content_type="application/json",
                         data=json.dumps(input_data))

        get_response = self.tester.post(self.meals_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_meals_no_meals(self):
        token = self.token
        expected_response_message = 'Meal not found'

        get_response = self.tester.get(self.meals_url, headers={'access-token':token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal_invalid_body_tag(self):
        token = self.token

        input_data = dict(name='meal', price=5000)
        update_data = dict(price1=6000)
        update_id = '1'
        update_url = self.meals_url + update_id

        expected_response_message = 'Invalid format.'

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token':token},
                         data=json.dumps(input_data))
        get_response = self.tester.put(update_url, content_type="application/json",
                        headers={'access-token':token}, data=json.dumps(update_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal_invalid_meal_id(self):
        token = self.token
        update_data = dict(price=6000)
        update_id = '1'
        update_url = self.meals_url + update_id

        expected_response_message = 'Meal not found.'

        get_response = self.tester.put(update_url, content_type="application/json",
                                       headers={'access-token': token}, data=json.dumps(update_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_empty_token(self):
        expected_response_message = 'Token required'
        get_response = self.tester.post(self.meals_url, headers={'access-token':''},
                                        content_type="application/json")

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(401, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_invalid_token(self):
        expected_response_message = 'Token is invalid'
        get_response = self.tester.post(self.meals_url, headers={'access-token':'hgsfajyasfjajkhafk'},
                                        content_type="application/json")

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(401, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_token_admin_rights(self):
        self.response = self.tester.post(self.login_url, content_type="application/json",
                                         data=json.dumps(self.login_data_user))

        self.response_results = json.loads(self.response.data.decode())
        self.token_user = self.response_results['token']

        expected_response_message = 'Action not allowed for this user'
        get_response = self.tester.post(self.meals_url, headers={'access-token':self.token_user},
                                        content_type="application/json")

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(401, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])



