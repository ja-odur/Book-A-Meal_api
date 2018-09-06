from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB
from app.v1.models.meal import Meal
from app.v1.models.caterer import Caterer
import unittest


class TestModelUserInfo(unittest.TestCase):
    def setUp(self):
        DB.create_all()

    def test_handles_integrity(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='default@example.com',
                                  username='default', brand_name='easy_caterer', password=12345,
                                  address='address')).add_caterer()
        caterer = Caterer.get_caterer(username='default')

        meal = Meal(name='test_meal', price='invalid_type').add_meal(caterer=caterer)
        Caterer.delete_caterer(username='default')
        self.assertFalse(meal)

    def test_handles_invalid_caterer_type(self):
        caterer = 'invalid_caterer_type'
        meal = Meal(name='test_meal', price=5000).add_meal(caterer=caterer)

        self.assertFalse(meal)

    def test_get_meals(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='default@example.com',
                                  username='default', brand_name='easy_caterer',
                                  password=12345, address='address')).add_caterer()
        caterer = Caterer.get_caterer(username='default')
        Caterer.delete_caterer(username='default')
        meals = Meal.get_meals(caterer)

        self.assertFalse(meals)

    def test_delete_meal_invalid_meal_id(self):
        deleted = Meal.delete_meal(meal_id=100)

        self.assertFalse(deleted)

    def test_invalid_missing_date(self):
        Caterer(caterer_data=dict(first_name='john', last_name='doe', email='default@example.com',
                                  username='default', brand_name='easy_caterer', password=12345,
                                  address='address')).add_caterer()
        caterer = Caterer.get_caterer(username='default')

        meal = Meal(name='test_meal', price=None).add_meal(caterer=caterer)
        Caterer.delete_caterer(username='default')

        self.assertFalse(meal)

    def test_handles_attribute_errors(self):
        caterer = "unsupported_type"
        meals = Meal.get_meals(caterer)

        self.assertFalse(meals)


