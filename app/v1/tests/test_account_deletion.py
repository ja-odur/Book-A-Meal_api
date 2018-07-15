import unittest
import json
from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB


URL_PREFIX = 'api/v1'


class TestAccountDeletion(unittest.TestCase):
    def setUp(self):
        DB.create_all()
        self.signup_url = URL_PREFIX + '/auth/signup'
        self.login_url = URL_PREFIX + '/auth/login'
        self.delete_url = URL_PREFIX +'/account'

        self.tester = app.test_client(self)

        self.reg_data = dict(category='caterer', email='caterer1@gmail.com', username='caterer1', password='12345',
                             confirm_password='12345', address='address1', first_name='odur', last_name='joseph')

        self.reg_data_user = dict(category='user', email='agnes@gmail.com', username='agnes', password='12345',
                                  confirm_password='12345', address='address1', first_name='agnes', last_name='a')

        self.login_data = dict(category='caterer', username='caterer1', password='12345')
        self.login_data_user = dict(category='user', username='agnes', password='12345')

        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(self.reg_data))
        self.tester.post(self.signup_url, content_type="application/json", data=json.dumps(self.reg_data_user))

        self.response = self.tester.post(self.login_url, content_type="application/json",
                                         data=json.dumps(self.login_data))
        self.response_user = self.tester.post(self.login_url, content_type="application/json",
                                         data=json.dumps(self.login_data_user))

        self.response_results = json.loads(self.response.data.decode())
        self.response_results_user = json.loads(self.response_user.data.decode())

        self.token_caterer = self.response_results['token']
        self.token_user = self.response_results_user['token']

    def tearDown(self):
        DB.drop_all()

    def test_deletion_user(self):
        response = self.tester.delete(self.delete_url, headers={'access-token':self.token_user})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual('Account successfully deleted', response_results['message'])

    def test_deletion_caterer(self):
        response = self.tester.delete(self.delete_url, headers={'access-token':self.token_caterer})

        response_results = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual('Account successfully deleted', response_results['message'])


