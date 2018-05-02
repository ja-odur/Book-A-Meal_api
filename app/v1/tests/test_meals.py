import unittest
import json

from run import app


class TestMeals(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        # self.get_response = None



    def test_create_meals(self):
        input_data = dict(username='default1', name='meal', price=5000)
        expected_response_message = 'Meal {} successfully added.'.format(input_data['name'])
        get_response = self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_all_meals(self):
        input_data = dict(username='default', name='meal', price=5000)
        expected_response_message = [[1, 'meal', 5000], [2, 'meal', 5000], [3, 'meal', 5000]]
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        get_response = self.tester.get('api/v1/meals/')

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_update_meal(self):
        input_data = dict(username='default', name='meal', price=5000)
        update_data = dict(price=6000)
        expected_response_message = [2, 'meal', 6000]
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        get_response = self.tester.put('api/v1/meals/2', content_type="application/json", data=json.dumps(update_data))


        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_delete_meal(self):
        input_data = dict(username='default', name='meal', price=5000)
        # update_data = dict(price=6000)
        expected_response_message = [[1, 'meal', 5000]]
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        self.tester.post('api/v1/meals/', content_type="application/json", data=json.dumps(input_data))
        get_response1 = self.tester.delete('api/v1/meals/2')
        get_response = self.tester.get('api/v1/meals/')

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])


if __name__ == '__main__':
    unittest.main()