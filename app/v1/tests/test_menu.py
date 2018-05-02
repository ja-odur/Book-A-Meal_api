import unittest
import json

from run import app

class TestMenu(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        # self.get_response = None



    def test_create_menu_successful(self):
        menu = [[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]]
        input_data = dict(menu=menu)
        expected_response_message = 'Menu {} successfully added.'.format(menu)
        get_response = self.tester.post('api/v1/menu/', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 201)
        self.assertEqual(expected_response_message, response_results['message'])
    def test_create_menu_failure(self):
        menu = dict(menu=[[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]])
        input_data = dict(menu=menu)
        expected_response_message =  'Bad data format'
        get_response = self.tester.post('api/v1/menu/', content_type="application/json", data=json.dumps(input_data))

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(expected_response_message, response_results['message'])

    def test_get_menu(self):
        menu = [[1, 'rice and posho', 5000], [2, 'rice and posho', 5000], [3, 'rice and posho', 5000]]
        return_dict = dict(default=menu)
        expected_response_message = 'Todays menu {}.'.format(return_dict)
        get_response = self.tester.get('api/v1/menu/')

        response_results = json.loads(get_response.data.decode())
        # print(response_results)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(expected_response_message, response_results['message'])

if __name__ == '__main__':
    unittest.main()
