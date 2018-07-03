from app.v1.models.db_connection import DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import datetime

from app.v1.models.caterer import Caterer


class Meal(DB.Model):
    """
        This class stores information about the meals offered by each registered caterer.
    """
    __tablename__ = 'meals'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120),nullable=False)
    long_name = DB.Column(DB.String(120), unique=True, nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
    point = DB.Column(DB.Integer, default=0)
    caterer = DB.Column(DB.Integer, DB.ForeignKey('caterers.id'))
    menu = DB.relationship('Menu', backref='menu')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    def add_meal(self, caterer):
        try:
            caterer_id = caterer.id
        except AttributeError:
            return False
        else:
            self.caterer = caterer_id
            self.long_name = '{}{}'.format(self.name, self.caterer)

            DB.session.add(self)

        return self.commit_changes()

    @staticmethod
    def update_meal(caterer, meal_id, value):
        caterer = Caterer.get_caterer(username=None, caterer_id=caterer.id)
        meal = Meal.get_meal(meal_id)
        if caterer:
            if meal and caterer.id == meal.caterer:
                if isinstance(value, str):
                    meal.name = value
                    return Meal.commit_changes()

                if isinstance(value, int):
                    meal.price = value
                    return Meal.commit_changes()
        return False

    @staticmethod
    def get_meal(meal_id):
        return Meal.query.filter_by(id=meal_id).first()

    @staticmethod
    def get_meals(caterer):
        meals = []
        raw_meals = Meal.query.filter_by(caterer=caterer.id)

        if raw_meals:
            for meal in raw_meals:
                meals.append(meal.to_dictionary())
            return meals
        return False

    @staticmethod
    def delete_meal(meal_id):
        meal = Meal.query.filter_by(id=meal_id).first()
        if meal:
            DB.session.delete(meal)
            return Meal.commit_changes()
        return False

    @staticmethod
    def easy_point(meal_id):
        meal = Meal.query.filter_by(id=meal_id).first()

        if meal:
            meal.point += 1
            return Meal.commit_changes()
        return False

    def to_dictionary(self):
        return dict(name=self.name, price=self.price, point=self.point, caterer=self.caterer, meal_id=self.id)

    def __repr__(self):
        return "Meal ->(name={}, price={})".format(self.name, self.price)


class Menu(DB.Model):
    """
        This class stores information about the menu of the day created by registered caterers.
    """
    __tablename__ = 'menus'
    id = DB.Column(DB.Integer, primary_key=True)
    meal = DB.Column(DB.Integer, DB.ForeignKey('meals.id'))
    order = DB.relationship('Order', backref='order')
    caterer = DB.Column(DB.Integer)

    def __init__(self, caterer_id, meal_id):
        self.caterer = caterer_id
        self.meal = meal_id

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    def add_meal_to_menu(self):
        meal = Meal.query.filter_by(id=self.meal).first()

        if not meal:
            return False
        if meal.caterer == self.caterer:
            DB.session.add(self)
            return Menu.commit_changes()
        return False

    @staticmethod
    def remove_meal_from_menu(caterer_id, meal_id):
        meal = Menu.query.filter_by(meal=meal_id).first()
        if not meal:
            return False
        if meal.caterer == caterer_id:
            DB.session.delete(meal)
            return Menu.commit_changes()
        return False

    @staticmethod
    def create_menu(caterer_id, *meal_ids):
        added_meals = []
        if not Caterer.query.filter_by(id=caterer_id).first():
            return False

        for meal_id in meal_ids:
            meal_added = Menu(caterer_id=caterer_id, meal_id=meal_id).add_meal_to_menu()

            if meal_added:
                added_meals.append(meal_id)

        if added_meals:
            return added_meals
        return False

    @staticmethod
    def delete_menu(caterer_id):
        menu = Menu.query.filter_by(caterer=caterer_id).all()
        print('menu_object', menu)
        print('all_menu_objects', Menu.query.all())
        if not menu:
            return False
        for menu_item in menu:
            DB.session.delete(menu_item)
        return Menu.commit_changes()

    @staticmethod
    def get_menu(caterer_id):
        menu = []
        raw_menu = Menu.query.filter_by(caterer=caterer_id)

        if not raw_menu:
            return False
        for menu_item in raw_menu:
            menu.append(
                dict(name=menu_item.menu.name, price=menu_item.menu.price, point=menu_item.menu.point,
                     caterer_id=menu_item.menu.caterer, menu_id=menu_item.id)
            )

        return menu

    @staticmethod
    def get_menus():
        all_menus = {}
        raw_menus = Menu.query.all()

        for menu_item in raw_menus:
            if menu_item.menu.caterer not in all_menus.keys():
                all_menus[menu_item.menu.caterer] = Menu.get_menu(caterer_id=menu_item.caterer)

        if all_menus:
            return all_menus
        return False

    def __repr__(self):
        return 'Menu Object'


class Order(DB.Model):
    """
    This class stores information about the orders made by registered users. Allows users to modify their orders
    if it's still within the one hour time lap. This orders information is stored in a two forms that are
    easily accessible by users (to view their orders) and caterers ( to view all the orders placed with them).
    """
    __tablename__ = 'orders'

    id = DB.Column(DB.Integer, primary_key=True)
    meal = DB.Column(DB.Integer, DB.ForeignKey('menus.id'), nullable=False)
    order_time = DB.Column(DB.DateTime, nullable=False)
    order_cleared = DB.Column(DB.Boolean, default=False)
    customer = DB.Column(DB.Integer, DB.ForeignKey('users.id'))

    ORDER_MODIFICATION_EXPIRY = datetime.timedelta(hours=1).total_seconds()

    def __init__(self, customer_id, meal_id):
        self.customer = customer_id
        self.meal = meal_id

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    def add_order(self):
        self.order_time = datetime.datetime.now()
        DB.session.add(self)
        return Order.commit_changes()

    @staticmethod
    def modify_order(customer_id, order_id, meal_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.customer != customer_id:
            return False

        elapsed_time = datetime.datetime.now() - order.order_time

        if elapsed_time.total_seconds() > Order.ORDER_MODIFICATION_EXPIRY:
            return False

        order.meal = meal_id
        return Order.commit_changes()

    @staticmethod
    def get_orders(customer_id=None, caterer_id=None):
        if customer_id:
            raw_orders = Order.query.filter_by(customer=customer_id)
            if raw_orders:
                orders = []
                for order in raw_orders:
                    orders.append(order.to_dictionary())
                return orders
            return False

        if caterer_id:
            raw_orders = Order.query.all()
            orders = []
            if raw_orders:
                for order in raw_orders:
                    if order.order.menu.caterer == caterer_id:
                        orders.append(order.to_dictionary())
                return orders
        return False

    @staticmethod
    def delete_order(customer_id, order_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.customer != customer_id:
            return False

        elapsed_time = datetime.datetime.now() - order.order_time

        if elapsed_time.total_seconds() > Order.ORDER_MODIFICATION_EXPIRY:
            return False

        DB.session.delete(order)
        return Order.commit_changes()

    @staticmethod
    def clear_order(caterer_id, order_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.order.menu.caterer == caterer_id:
            order.order_cleared = True
            return Order.commit_changes()
        return False

    @staticmethod
    def get_order_history(customer_id):
        orders = Order.query.filter_by(customer=customer_id)

        if not orders:
            return False
        order_history = []

        for order in orders:
            if order.order_cleared:
                order_history.append(order.to_dictionary())
        return order_history

    def to_dictionary(self):
        return dict(order_id=self.id, meal=self.order.menu.name, price=self.order.menu.price,
                    order_cleared=self.order_cleared, customer_id=self.customer, caterer_id=self.order.menu.caterer)
