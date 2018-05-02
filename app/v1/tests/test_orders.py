import unittest
import json


from run import app


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        # self.get_response = None

    def test_create_order_success(self):
        order = dict(meal=[1, 'rice and posho', 5000], caterer='default')
        order1 = dict(meal=[1, 'rice and posho', 5000], caterer='default4')

        expected_response_message = 'Order {} successfully placed.'.format(order)
        self.tester.post('api/v1/orders', content_type="application/json", data=json.dumps(order1))

        get_response = self.tester.post('api/v1/orders', content_type="application/json", data=json.dumps(order))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_create_order_failure(self):
        order = dict(meal3=[1, 'rice and posho', 5000], caterer='default3')

        expected_response_message = 'Invalid request format'
        get_response = self.tester.post('api/v1/orders', content_type="application/json", data=json.dumps(order))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_modify_order(self):
        modified_order = dict(meal=[1, 'rice and posho_modified', 5000], caterer='default4')
        expected_response_message = 'Order {} successfully modified.'.format(modified_order)

        # self.tester.post('api/v1/orders', content_type="application/json", data=json.dumps(order))
        get_response = self.tester.put('api/v1/orders/1', content_type="application/json",
                                       data=json.dumps(modified_order))

        response_results = json.loads(get_response.data.decode())
        print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])



    def test_get_all_orders_failure(self):
        expected_response_message = 'Oops, orders not found.'
        get_response = self.tester.get('api/v1/orders')

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_orders_successful(self):
        order = dict(meal=[1, 'rice and posho', 5000], caterer='default10')
        expected_response_message = 'The request was successfull'
        self.tester.post('api/v1/orders', content_type="application/json", data=json.dumps(order))
        get_response = self.tester.get('api/v1/orders')

        response_results = json.loads(get_response.data.decode())

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(expected_response_message, response_results['message'])


if __name__ == '__main__':
    unittest.main()