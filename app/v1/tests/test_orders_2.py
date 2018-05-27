import unittest
import json
from run import app


class TestOrders2(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.reg_data = dict(category='caterer', email='odur@gmail.com', username='odur', password='12345',
                             confirm_password='12345', address='address1')
        self.reg_data_user = dict(category='user', email='defaultUser@gmail.com', username='defaultUser',
                                  password='12345', confirm_password='12345', address='address1')

        self.login_data_user = dict(category='user', username='defaultUser', password='12345')
        self.login_data_caterer = dict(category='caterer', username='odur', password='12345')

        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post('api/v1/auth/signup', content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response_user = self.tester.post('api/v1/auth/login', content_type="application/json",
                                         data=json.dumps(self.login_data_user))
        self.response_caterer = self.tester.post('api/v1/auth/login', content_type="application/json",
                                              data=json.dumps(self.login_data_caterer))

        self.response_results_user = json.loads(self.response_user.data.decode())
        self.response_results_caterer = json.loads(self.response_caterer.data.decode())
        # print('user response', self.response_results_user)
        # print('caterer response', self.response_results_caterer)

        self.token_user = self.response_results_user['token']
        self.token_caterer = self.response_results_caterer['token']

        # print('user', self.token_user)
        # print('caterer', self.token_caterer)

    def test_clear_order(self):
        token_user = self.token_user
        token_caterer = self.token_caterer
        expected_response_message = ''
        order1 = dict(meal=[1, 'rice and beef', 10000], caterer='default22')
        order2 = dict(meal=[1, 'matooke and beef', 5000], caterer='default22')

        self.tester.post('api/v1/orders', headers={'access-token': token_user},
                         content_type="application/json", data=json.dumps(order1))
        self.tester.post('api/v1/orders', headers={'access-token': token_user},
                         content_type="application/json", data=json.dumps(order2))

        self.tester.patch('api/v1/orders/clear/1', headers={'access-token':token_user})

        response = self.tester.get('api/v1/orders/placed', headers={'access-token': token_user})
        response_results = json.loads(response.data.decode())
        print(response_results['message'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response_message, len(response_results['message']))


if __name__ == '__main__':
    unittest.main()