from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB
from app.v1.models.user import User
from app.v1.models.caterer import Caterer
import unittest


class TestModelCaterer(unittest.TestCase):
    def setUp(self):
        DB.create_all()

    def test_handles_integrity(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='johndoe1@example.com',
                                  username='johndoegdsahjasmhakjda,ksakasjhgkasFGJDSAFMNBFKJhgadsnmbafsdjhbkajkhabnmba'
                                           'jkhsdajkhasdklhasdjhdasklaskladskjklsdauafshjklasflkhfsahklasf',
                                  password=12345, address='address', brand_name='easy_caterer')).add_caterer()

        caterers = Caterer.get_caterers()

        self.assertEquals(0, len(caterers))

    def test_delete_user(self):
        User(first_name='john', last_name='doe', email='johndoe10@example.com', username='johndoe10', password=12345,
             address='address', brand_name='easy_caterer').add_user()
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='johndoe10@example.com',
                                  username='johndoe10', password=12345, address='address',
                                  brand_name='easy_caterer')).add_caterer()

        deleted = Caterer.delete_caterer(username='johndoe10')
        self.assertTrue(deleted)

    def test_get_invalid_caterer(self):
        caterer = Caterer.get_caterer(username='non_exiting_username')

        self.assertFalse(caterer)

    def test_duplicate_creation(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='johndoe1@example.com',
                                  username='johndoe',password=12345, address='address',
                                  brand_name='easy_caterer')).add_caterer()
        caterer = Caterer(caterer_data=dict(first_name='john', last_name='doe', email='johndoe1@example.com',
                                            username='johndoe',password=12345, address='address',
                                            brand_name='easy_caterer')).add_caterer()
        Caterer.delete_caterer(username='johndoe')

        self.assertFalse(caterer)

