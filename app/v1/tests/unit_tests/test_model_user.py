from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB
from app.v1.models.user import User
from app.v1.models.caterer import Caterer
import unittest


class TestModelUser(unittest.TestCase):
    def setUp(self):
        DB.create_all()

    def tearDown(self):
        User.delete_user(username='johndoe')
        Caterer.delete_caterer(username='johndoe5')

    def test_get_users(self):
        User(first_name='john', last_name='doe', email='johndoe@example.com', username='johndoe', password=12345,
             address='address').add_user()
        users = User.get_users()
        User.delete_user(username='johndoe')

        self.assertEquals('johndoe', users[0]['username'])


    def test_handles_integrity(self):
        User(first_name='john', last_name='doe', email='johndoe1@example.com', username='johndoegdsahjasmhakjda,ksakasj'
             'hgkasFGJDSAFMNBFKJhgadsnmbafsdjhbkajkhabnmbajkhsdajkhasdklhasdjhdasklaskladskjklsdauafshjklasflkhf'
             'sahklasf', password=12345, address='address').add_user()

        users = User.get_users()

        self.assertEquals(0, len(users))

    def test_delete_user(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='johndoe5@example.com',
                                  username='johndoe5', password=12345, address='address')).add_caterer()
        User(first_name='john', last_name='doe', email='johndoe5@example.com', username='johndoe5', password=12345,
             address='address').add_user()

        deleted = User.delete_user(username='johndoe5')
        Caterer.delete_caterer(username='johndoe5')
        self.assertTrue(deleted)

    def test_delete_invalid_user(self):
        deleted = User.delete_user(username='unkonwn_user')
        self.assertFalse(deleted)



