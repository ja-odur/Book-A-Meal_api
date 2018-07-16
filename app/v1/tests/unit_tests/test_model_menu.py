from app.v1.tests.test_app import app
from app.v1.models.db_connection import DB
from app.v1.models.menu import Menu
import unittest


class TestModelMenu(unittest.TestCase):
    def setUp(self):
        DB.create_all()

    def test_handles_integrity(self):
        menu = Menu(caterer_id=100, meal_id=100).add_meal_to_menu()

        self.assertFalse(menu)

    def test_create_menu_false(self):
        menu = Menu.create_menu(None, 12, 15)

        self.assertFalse(menu)

