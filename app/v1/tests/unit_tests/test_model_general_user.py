from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB
from app.v1.models.general_users_info import UserInfo
import unittest


class TestModelUserInfo(unittest.TestCase):
    def setUp(self):
        DB.create_all()

    def test_get_users(self):
        UserInfo(email='default@example.com', first_name='john', last_name='doe',
                 address='No address provided').add_user()

        users = UserInfo.get_users()
        UserInfo.delete_user(user_id=None, email='default@example.com')

        self.assertEquals('default@example.com', users[-1]['email'])

    def test_handles_integrity(self):
        user = UserInfo(email='default@example.com', first_name='johnjkn,msdnladn.m,dsgalkngmnkjefn sjkbsmgn,wnkjsnf,ns'
                                                         'hbmngbsjhbsm,gnaskgjdkbfhjgjkadhjghjkgsdjhkjhgjhgskhgbkjg'
                                                         'jhsdnbahjgajkbnakhgkjagnjkahgjhajkhgabgjhagjagjhaghjjkga'
                                                         'hbgshjkgahjbnajhgjsdngbsjdghjksgdbhjadhjkabhjfdhj',
                        last_name='doe', address='No address provided').add_user()

        self.assertFalse(user)

    def test_get_user(self):
        UserInfo(email='default@example.com', first_name='john', last_name='doe',
                 address='No address provided').add_user()
        user = UserInfo.get_user(user_id=None, email='default@example.com')
        print(user)

        same_user = UserInfo.get_user(user_id=user.user_id)
        UserInfo.delete_user(user_id=None, email='default@example.com')

        self.assertEquals(user, same_user)

    def test_delete_invalid_user(self):
        deleted = UserInfo.delete_user(user_id=None, email='unknown_user_email@example.com')

        self.assertFalse(deleted)




