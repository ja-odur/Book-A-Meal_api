import unittest
import json

from run import app


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='default22@gmail.com', username='default22', password='12345',
                             confirm_password='12345', address='address1')
        self.reg_data_empty = dict(category='caterer', email='default@gmail.com', username='default',
                                   password='12345', confirm_password='12345', address='address1')

        self.reg_data_user = dict(category='user', email='defaultuser@gmail.com', username='defaultuser',
                                  password='12345', confirm_password='12345', address='address1')

        self.login_data = dict(category='caterer', username='default22', password='12345')
        self.login_data_user = dict(category='user', username='defaultuser', password='12345')

        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data_user))
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data_empty))

        self.response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_user = self.tester.post('api/v1/auth/login', content_type="application/json",
                                              data=json.dumps(self.login_data_user))

        self.response_results = json.loads(self.response.data.decode())
        self.response_results_user = json.loads(self.response_user.data.decode())

        print('user', self.response_results_user)
        print('caterer', self.response_results)

        self.token = self.response_results['token']
        self.token_user = self.response_results_user['token']

    def test_create_order_success(self):
        token_user = self.token_user
        order = dict(meal=[1, 'rice and posho', 5000], caterer='default22')
        order1 = dict(meal=[1, 'rice and posho', 5000], caterer='default22')

        expected_response_message = 'Order {} successfully placed.'.format(order)
        self.tester.post('api/v1/orders', headers={'access-token':token_user},
                         content_type="application/json", data=json.dumps(order1))

        get_response = self.tester.post('api/v1/orders', headers={'access-token':token_user},
                                        content_type="application/json", data=json.dumps(order))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_order_failure(self):
        token_user = self.token_user
        order = dict(meal3=[1, 'rice and posho', 5000], caterer='default3')

        expected_response_message = 'Invalid request format'
        get_response = self.tester.post('api/v1/orders', headers={'access-token':token_user},
                                        content_type="application/json", data=json.dumps(order))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order(self):
        token_user = self.token_user
        modified_order = dict(meal=[1, 'rice and posho_modified', 5000], caterer='default22')
        expected_response_message = 'Order {} successfully modified.'.format(modified_order)

        get_response = self.tester.put('api/v1/orders/1', content_type="application/json", headers={'access-token':token_user},
                                       data=json.dumps(modified_order))

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_orders_failure(self):
        login_data = dict(category='caterer', username='default', password='12345')

        response = self.tester.post('api/v1/auth/login', content_type="application/json",
                                    data=json.dumps(login_data))

        response_results = json.loads(response.data.decode())
        print('response from login', response_results)
        token_caterer = response_results['token']

        expected_response_message = 'Oops, orders not found.'
        get_response = self.tester.get('api/v1/orders', headers={'access-token':token_caterer})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_orders_successful(self):
        token_caterer = self.token
        order = dict(meal=[1, 'rice and posho', 5000], caterer='default22')
        expected_response_message = 'The request was successfull'
        self.tester.post('api/v1/orders', content_type="application/json", headers={'access-token':token_caterer},
                         data=json.dumps(order))
        get_response = self.tester.get('api/v1/orders', headers={'access-token':token_caterer})

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_orders(self):
        token_user = self.token_user
        expected_response_message = 1
        response = self.tester.get('api/v1/orders/placed', headers={'access-token': token_user})

        response_results = json.loads(response.data.decode())
        # print('response result', response_results['message'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response_message, len(response_results['message']))

    def test_delete_order(self):
        token_user = self.token_user
        expected_response_message = 1

        response22 = self.tester.get('api/v1/orders/placed', headers={'access-token': token_user})
        response_results1 = json.loads(response22.data.decode())
        # print('response result', response_results1['message'])

        self.tester.delete('api/v1/orders/2', headers={'access-token':token_user})
        response = self.tester.get('api/v1/orders/placed', headers={'access-token':token_user})
        response_results = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response_message, len(response_results['message']))


if __name__ == '__main__':
    unittest.main()