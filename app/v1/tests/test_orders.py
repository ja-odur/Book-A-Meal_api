import unittest
import json

from run import app
from app.v1.models.db_connection import DB

URL_PREFIX = 'api/v1'


class TestOrder(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        signup_url = URL_PREFIX + '/auth/signup'
        login_url = URL_PREFIX + '/auth/login'
        self.meals_url = URL_PREFIX + '/meals/'
        self.menu_url = URL_PREFIX + '/menu/'
        self.order_url = URL_PREFIX + '/orders'

        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                             confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        self.reg_data_user = dict(category='user', email='user1@gmail.com', username='user1', password='12345',
                                  confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        self.login_data = dict(category='caterer', username='caterer1', password='12345')
        self.login_data_user = dict(category='user', username='user1', password='12345')

        self.tester.post(signup_url, content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post(signup_url, content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response = self.tester.post(login_url, content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_user = self.tester.post(login_url, content_type="application/json",
                                              data=json.dumps(self.login_data_user))

        self.response_caterer = json.loads(self.response.data.decode())
        self.response_user = json.loads(self.response_user.data.decode())

        self.token_caterer = self.response_caterer['token']
        self.token_user = self.response_user['token']

        meal_data1 = dict(name='meal', price=5000)
        meal_data2 = dict(name='meal2', price=10000)

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': self.token_caterer},
                         data=json.dumps(meal_data1))
        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': self.token_caterer},
                         data=json.dumps(meal_data2))

    def tearDown(self):
        DB.drop_all()

    def test_create_order_success(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        expected_response_message = 'Order successfully placed.'
        self.tester.post(self.order_url + '/1', headers={'access-token':self.token_user})

        get_response = self.tester.post(self.order_url + '/2', headers={'access-token':self.token_user})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(201, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_order_failure_invalid_meal_id(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        expected_response_message = 'Order not placed'
        get_response = self.tester.post(self.order_url + '/3', headers={'access-token':self.token_user})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order(self):
        meal_data3 = dict(name='meal3_modified', price=15000)

        expected_response_message = 'Order successfully modified.'

        self.tester.post(self.meals_url, content_type="application/json", headers={'access-token': self.token_caterer},
                         data=json.dumps(meal_data3))

        meal_ids = dict(meal_ids=[1, 2, 3])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/2', headers={'access-token': self.token_user})

        get_response = self.tester.put(self.order_url + '/1', headers={'access-token': self.token_user},
                                       content_type="application/json", data=json.dumps(dict(meal_id=3)))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(201, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_no_order_found(self):
        expected_response_message = 'Oops, orders not found.'
        get_response = self.tester.get(self.order_url, headers={'access-token':self.token_caterer})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_orders_per_caterer_works(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/1', headers={'access-token': self.token_user})

        expected_response_message = {'content': [{'caterer_id': 1, 'customer_id': 1, 'meal': 'meal',
                                                  'order_cleared': False, 'order_id': 1, 'price': 5000}]}

        get_response = self.tester.get(self.order_url, headers={'access-token':self.token_caterer})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(200, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_orders_placed_customer(self):
        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/1', headers={'access-token': self.token_user})
        expected_response_message = 1
        response = self.tester.get(self.order_url + '/placed', headers={'access-token': self.token_user})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response_message, len(response_results['message']))

    def test_delete_order(self):
        expected_response_message = 1

        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/1', headers={'access-token': self.token_user})

        self.tester.post(self.order_url + '/2', headers={'access-token': self.token_user})

        self.tester.delete(self.order_url + '/1', headers={'access-token':self.token_user})
        response = self.tester.get(self.order_url + '/placed', headers={'access-token':self.token_user})
        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response_message, len(response_results['message']))

    def test_clear_order(self):
        expected_response_message = True

        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/1', headers={'access-token': self.token_user})

        self.tester.patch(self.order_url + '/clear/1', headers={'access-token':self.token_caterer})

        response = self.tester.get(self.order_url + '/placed', headers={'access-token': self.token_user})
        response_results = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'][0]['order_cleared'])

    def test_clear_order_invalid_order_id(self):
        expected_response_message = 'Order does not exist'

        response = self.tester.patch(self.order_url + '/clear/1', headers={'access-token':self.token_caterer})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_history(self):
        expected_result = True
        expected_length = 1

        meal_ids = dict(meal_ids=[1, 2])

        self.get_response = self.tester.post(self.menu_url, headers={'access-token': self.token_caterer},
                                             content_type="application/json", data=json.dumps(meal_ids))

        self.tester.post(self.order_url + '/1', headers={'access-token': self.token_user})

        self.tester.patch(self.order_url + '/clear/1', headers={'access-token':self.token_caterer})

        history_response = self.tester.get(self.order_url + '/history', headers={'access-token': self.token_user})
        history = json.loads(history_response.data.decode())

        self.assertEqual(200, history_response.status_code)
        self.assertEqual(expected_length, len(history['message']))
        self.assertEqual(expected_result, history['message'][0]['order_cleared'])

    def test_create_order_caterer(self):

        expected_response_message = 'Caterers can not create an order'

        get_response = self.tester.post(self.order_url + '/2', headers={'access-token':self.token_caterer})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(403, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_order_invalid_data_format(self):

        expected_response_message = 'Order not placed'

        get_response = self.tester.post(self.order_url + '/2', headers={'access-token':self.token_user})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order_caterer(self):

        expected_response_message = 'Caterers can not modify an order'

        get_response = self.tester.put(self.order_url + '/1', headers={'access-token': self.token_caterer},
                                       content_type="application/json", data=json.dumps(dict(meal_id=3)))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(403, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_history_caterer(self):
        expected_result = 'Sorry operation not permitted for caterers.'

        history_response = self.tester.get(self.order_url + '/history', headers={'access-token': self.token_caterer})
        history = json.loads(history_response.data.decode())

        self.assertEqual(403, history_response.status_code)
        self.assertEqual(expected_result, history['message'])

    def test_get_empty_history(self):
        expected_result = 'No order history'

        history_response = self.tester.get(self.order_url + '/history', headers={'access-token': self.token_user})
        history = json.loads(history_response.data.decode())

        self.assertEqual(200, history_response.status_code)
        self.assertEqual(expected_result, history['message'])

    def test_delete_order_caterer(self):
        expected_response_message = 'This method is meant for customers only'
        response = self.tester.delete(self.order_url + '/1', headers={'access-token':self.token_caterer})

        response_results = json.loads(response.data.decode())

        self.assertEqual(403, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_order_invalid_order_id(self):
        expected_response_message = 'Order not found'
        response = self.tester.delete(self.order_url + '/5', headers={'access-token':self.token_user})

        response_results = json.loads(response.data.decode())

        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_orders_placed_caterer(self):
        expected_response_message = 'This method is meant for customers only'

        response = self.tester.get(self.order_url + '/placed', headers={'access-token': self.token_caterer})

        response_results = json.loads(response.data.decode())

        self.assertEqual(403, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_orders_no_placed_order(self):
        expected_response_message = 'No orders placed'

        response = self.tester.get(self.order_url + '/placed', headers={'access-token': self.token_user})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order_invalid_order_id(self):
        expected_response_message = 'Resource not found'
        get_response = self.tester.put(self.order_url + '/1', headers={'access-token': self.token_user},
                                       content_type="application/json", data=json.dumps(dict(meal_id=3)))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(404, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order_missing_key(self):
        expected_response_message = 'Invalid request format'
        get_response = self.tester.put(self.order_url + '/1', headers={'access-token': self.token_user},
                                       content_type="application/json", data=json.dumps(dict(meal=3)))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(400, get_response.status_code)
        self.assertEqual(expected_response_message, response_results['message'])


# if __name__ == '__main__':
#     unittest.main()