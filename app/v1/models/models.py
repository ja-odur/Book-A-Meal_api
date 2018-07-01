from app.v1.models.db_connection import DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
import datetime


class UserInfo(DB.Model):
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the database.
    """
    __tablename__ = 'users_info'
    user_id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    first_name = DB.Column(DB.String(60), nullable=False)
    last_name = DB.Column(DB.String(254), nullable=False)
    address = DB.Column(DB.String(254))
    user_counter = DB.Column(DB.Integer, default=1)
    caterer = DB.relationship('Caterer', backref='caterer')
    customer = DB.relationship('User', backref='customer')

    def __init__(self, email, first_name, last_name, address='No address provided'):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @staticmethod
    def to_dictionary(user_object):
        if isinstance(user_object, UserInfo):
            return dict(first_name=user_object.first_name, last_name=user_object.last_name, email=user_object.email,
                        address=user_object.address)
        return False

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    @staticmethod
    def get_user(user_id, email=None):
        if email:
            user = UserInfo.query.filter_by(email=email).first()

        else:
            user = UserInfo.query.filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserInfo.query.filter_by(user_id=user_id).first()
        try:
            DB.session.delete(user)
        except UnmappedInstanceError:
            return False
        else:
            return UserInfo.commit_changes()

    @staticmethod
    def get_users():
        return UserInfo.query.all()

    def add_user(self):
        user = DB.session.add(self)

        if self.commit_changes():
            return True
        return False

    def __repr__(self):
        return "User info ->(email={}, first_name={}, last_name={}, address={})".format(self.email, self.first_name,
                                                                                        self.last_name,
                                                                                        self.address)


class User(DB.Model):
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the database.
    """
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(60), unique=True)
    email = DB.Column(DB.String(160), unique=True)
    password = DB.Column(DB.String(254), nullable=False)
    user = DB.Column(DB.Integer, DB.ForeignKey('users_info.user_id'))
    order = DB.relationship('Order', backref='client')

    def __init__(self, first_name, last_name, email, username, password, address='No address provided'):
        self.email = email
        self.username = username
        self.password = password
        self.address = address
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def to_dictionary(user_object):
        if isinstance(user_object, User):
            return dict(username=user_object.username, email=user_object.email, address=user_object.address,
                        user_id=user_object.id)
        return False

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    @staticmethod
    def get_user(username, email=None, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()

        elif email:
            user = User.query.filter_by(email=email).first()
        else:
            user = User.query.filter_by(username=username).first()
        if user:
            return user
        return False

    @staticmethod
    def delete_user(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return False
        counter = user.customer.user_counter
        if counter <= 1:
            UserInfo.delete_user(user.customer.user_id)
        else:
            user.customer.user_counter -= 1
            DB.session.commit()
        try:
            DB.session.delete(user)
        except UnmappedInstanceError:
            return False
        else:
            return User.commit_changes()

    @staticmethod
    def get_users():
        return User.query.all()

    def add_user(self):
        users = self.get_users()
        for user in users:
            if user.email == self.email or user.username == self.username:
                return False

        user_info = UserInfo.query.filter_by(email=self.email).first()

        if user_info:
            user_info.user_counter += 1
            self.user = user_info.user_id
            return self.save()
        else:
            new_user_info = UserInfo(email=self.email, first_name=self.first_name, last_name=self.last_name,
                                     address=self.address).add_user()
            if new_user_info:
                self.user = UserInfo.query.filter_by(email=self.email).first().user_id
                if self.save():
                    return True
        return False

    def save(self):
        DB.session.add(self)
        return self.commit_changes()

    def __repr__(self):
        try:
            return "User->(email={}, username={}, first_name={}, last_name={}," \
               " address={})".format(self.email, self.username, self.customer.first_name, self.customer.last_name,
                                     self.customer.address)
        except AttributeError:
            return "User to created->(email={}, username={}, first_name={}, last_name={}" \
               ")".format(self.email, self.username, self.first_name, self.last_name)


class Caterer(DB.Model):
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the database.
    """
    __tablename__ = 'caterers'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(60), unique=True)
    email = DB.Column(DB.String(160), unique=True)
    password = DB.Column(DB.String(254), nullable=False)
    user = DB.Column(DB.Integer, DB.ForeignKey('users_info.user_id'))
    meal = DB.relationship('Meal', backref='meal')

    def __init__(self, first_name, last_name, email, username, password, address='No address provided'):
        self.email = email
        self.username = username
        self.password = password
        self.address = address
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    @staticmethod
    def get_caterer(username, email=None, caterer_id=None):
        if caterer_id:
            caterer = Caterer.query.filter_by(id=caterer_id).first()

        elif email:
            caterer = Caterer.query.filter_by(email=email).first()
        else:
            caterer = Caterer.query.filter_by(username=username).first()
        if caterer:
            return caterer
        return False

    @staticmethod
    def delete_caterer(username):
        caterer = Caterer.query.filter_by(username=username).first()
        if not caterer:
            return False
        counter = caterer.caterer.user_counter
        if counter <= 1:
            UserInfo.delete_user(caterer.caterer.user_id)
        else:
            caterer.caterer.user_counter -= 1
            DB.session.commit()
        try:
            DB.session.delete(caterer)
        except UnmappedInstanceError:
            return False
        else:
            return Caterer.commit_changes()

    @staticmethod
    def get_caterers():
        return Caterer.query.all()

    def add_caterer(self):
        caterers = self.get_caterers()
        for caterer in caterers:
            if caterer.email == self.email or caterer.username == self.username:
                return False

        user_info = UserInfo.query.filter_by(email=self.email).first()
        if user_info:
            user_info.user_counter += 1
            self.user = user_info.user_id
            return self.save()
        else:
            new_user_info = UserInfo(email=self.email, first_name=self.first_name, last_name=self.last_name,
                                     address=self.address).add_user()
            if new_user_info:
                self.user = UserInfo.query.filter_by(email=self.email).first().user_id
                if self.save():
                    return True
        return False

    def save(self):
        DB.session.add(self)
        return self.commit_changes()

    def __repr__(self):
        try:
            return "Caterer->(email={}, username={}, first_name={}, last_name={}," \
               " address={})".format(self.email, self.username, self.caterer.first_name, self.caterer.last_name,
                                     self.caterer.address)
        except AttributeError:
            return "Caterer to created->(email={}, username={}, first_name={}, last_name={}" \
                   ")".format(self.email, self.username, self.first_name, self.last_name)


class Meal(DB.Model):
    """
        This class stores information about the meals offered by each registered caterer.
    """
    __tablename__ = 'meals'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True, nullable=False)
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
        meal = Menu.query.filter_by(id=meal_id).first()
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
        menu = Menu.query.filter_by(caterer=caterer_id)
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
                     caterer_id=menu_item.menu.caterer)
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


DB.create_all()
