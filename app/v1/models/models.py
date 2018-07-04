from app.v1.models.db_connection import DB
from app.v1.models.user import User
from app.v1.models.caterer import Caterer
from app.v1.models.meal import Meal
from app.v1.models.menu import Menu
from app.v1.models.order import Order

DB.create_all()
