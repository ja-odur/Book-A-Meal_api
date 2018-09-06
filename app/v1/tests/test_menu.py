import unittest
import json

from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB

URL_PREFIX = 'api/v1'


class TestMenu(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        self.signup_url = URL_PREFIX + '/auth/signup'
        self.login_url = URL_PREFIX + '/auth/login'
        self.meals_url = URL_PREFIX + '/meals/'
        self.menu_url = URL_PREFIX + '/menu/'

        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                            confirm_password='12345', address='address1', brand_name='easy_caterer',
                             first_name='odur', last_name='joseph')
        self.login_data = dict(category='caterer', username='caterer1', password='12345')

        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(self.reg_data))
        self.response = self.tester.post(self.login_url, content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_results = json.loads(self.response.data.decode())
        self.token = self.response_results['token']

        meal_data1 = dict(name='meal1', price=5000)
        meal_data2 = dict(name='meal2', price=5000)

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': self.token},
                         data=json.dumps(meal_data1))
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': self.token},
                         data=json.dumps(meal_data2))



    def tearDown(self):
        DB.drop_all()

    def test_create_menu_successful(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token},
                                             content_type="application/json", data=json.dumps(meal_ids))

        expected_response_message = 'Menu successfully created.'

        response_results = json.loads(self.get_response.data.decode())

        self.assertEqual(201, self.get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_menu_missing_meal_ids(self):
        token = self.token
        menu = dict(menu=[[3, 'rice and posho', 5000]])
        input_data = dict(menu=menu)
        expected_response_message = 'Bad data format'
        get_response = self.tester.post(self.menu_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_menu_bad_format(self):
        token = self.token
        input_data = dict(meal_ids=1)

        expected_response_message = 'Please submit a list of meal ids.'
        get_response = self.tester.post(self.menu_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_menu_invalid_meal_id(self):
        token = self.token
        input_data = dict(meal_ids=[5, 6])

        expected_response_message = 'Menu not created.'
        get_response = self.tester.post(self.menu_url, headers={'access-token':token},
                                        content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_menu(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token},
                                             content_type="application/json", data=json.dumps(meal_ids))

        expected_response_message = {'MENU': {'easy_caterer': [{'brand_name': 'easy_caterer', 'caterer_id': 1,
                                                                'meal_id': 1, 'menu_id': 1, 'name': 'meal1',
                                                                'point': 0, 'price': 5000},
                                                               {'brand_name': 'easy_caterer', 'caterer_id': 1,
                                                                'meal_id': 2, 'menu_id': 2, 'name': 'meal2',
                                                                'point': 0, 'price': 5000}]}}
        
        get_response = self.tester.get('api/v1/menu/', headers={'access-token':self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_menu_failure(self):

        expected_response_message = 'Menu not found.'

        get_response = self.tester.get('api/v1/menu/', headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_remove_meal_from_menu_successful(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token},
                                             content_type="application/json", data=json.dumps(meal_ids))

        get_response = self.tester.delete('api/v1/menu/meal/1', headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual('Meal successfully removed from menu.', response_results['message'])

    def test_remove_meal_from_menu_failure(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token},
                                             content_type="application/json", data=json.dumps(meal_ids))

        get_response = self.tester.delete('api/v1/menu/meal/3', headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual('Meal not removed', response_results['message'])

    def test_delete_menu_successful(self):
        meal_ids = dict(meal_ids=[1, 2])
        reg_data = dict(category='caterer', email='caterer2@gmail.com', username='caterer2', password='12345',
                             confirm_password='12345', address='address1', brand_name='easy_caterer1',
                        first_name='odur', last_name='joseph')
        login_data = dict(category='caterer', username='caterer2', password='12345')

        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(reg_data))

        response1 = self.tester.post(self.login_url, content_type="application/json",
                                         data=json.dumps(login_data))
        response_results1 = json.loads(response1.data.decode())
        token_caterer2 = response_results1['token']

        meal_data1 = dict(name='meal3', price=5000)
        meal_data2 = dict(name='meal4', price=5000)

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': token_caterer2},
                         data=json.dumps(meal_data1))
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': token_caterer2},
                         data=json.dumps(meal_data2))

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': token_caterer2},
                                             content_type="application/json", data=json.dumps(dict(meal_ids=[2,3])))

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token},
                                             content_type="application/json", data=json.dumps(meal_ids))

        get_response = self.tester.delete('api/v1/menu/', headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual('Menu deleted', response_results['message'])

    def test_delete_menu_failure(self):
        get_response = self.tester.delete('api/v1/menu/', headers={'access-token': self.token})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual('No menu found', response_results['message'])


