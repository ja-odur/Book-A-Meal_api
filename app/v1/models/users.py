from app.v1.models.db_connection import DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


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
        print(user)
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
        return user

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
        print('user', user_info)
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
        return "User->(email={}, username={}, first_name={}, last_name={}," \
               " address={})".format(self.email, self.username, self.customer.first_name, self.customer.last_name,
                                     self.customer.address)


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
        return caterer

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
        print('user', user_info)
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
        return "Caterer->(email={}, username={}, first_name={}, last_name={}," \
               " address={})".format(self.email, self.username, self.caterer.first_name, self.caterer.last_name,
                                     self.caterer.address)

class DbMeals:
    """
    This class stores information about the meals offered by registered caterers.
    """
    def __init__(self):
        self.meals = dict()
        self.meal_id = 1

    def add_meal(self, caterer, meal_name, price):
        caterer_meals = self.meals.get(caterer, False)

        if not caterer_meals:
            meals = list()
            meal_id = self.meal_id
            easy_point = 0
            meal = [meal_id, meal_name, price, easy_point, caterer]
            meals.append(meal)

            self.meals[caterer] = meals
            self.meal_id += 1
            return True

        else:
            all_meals = self.meals[caterer]
            meal_id = self.meal_id
            # meal_id = all_meals[-1][0] + 1
            easy_point = 0
            all_meals.append([meal_id, meal_name, price, easy_point, caterer])
            self.meal_id += 1
            return True

        # for any reason meal not added
        return False

    def get_meal(self, caterer, meal_id):
        all_meals_caterer = self.get_all_meals(caterer)
        if not all_meals_caterer:
            return False
        else:
            length = len(all_meals_caterer)

        if isinstance(meal_id, int) and meal_id > 0:
            actual_id = meal_id -1
        else:
            return False

        if actual_id <= length:
            meal = all_meals_caterer[meal_id - 1]
            return meal

        return False

    def update_meal(self, caterer, meal_id, field_to_update, new_value):
        meal = self.get_meal(caterer, meal_id)
        if meal:
            if field_to_update == 'name':
                if isinstance(new_value, str):
                    meal[1] = new_value
            elif field_to_update == 'price':
                meal[2] = new_value
            self.get_all_meals(caterer)[meal_id-1] = meal
            return meal
        return False

    def get_all_meals(self, caterer):
        meals = self.meals.get(caterer, False)
        return meals

    def delete_meal(self, caterer, meal_id):
        deleted = False
        all_meals = self.get_all_meals(caterer)

        if all_meals:
            counter = 0
            list_length = len(all_meals)

            while counter < list_length:
                meal = all_meals[counter]

                if meal[0] == meal_id:
                    deleted = True
                    break

                counter += 1
            if deleted:
                del self.meals[caterer][counter]
                return True

        return False

    def easy_point(self, meal_id):
        all_meals = self.meals

        for meals in all_meals.values():
            for meal in meals:
                if meal[0] == meal_id:
                    meal[3] += 1
                    return True
        return False


class Meal(DB.Model):
    """
        This class stores information about the meals offered by each registered caterer.
        """
    __tablename__ = 'meals'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
    point = DB.Column(DB.Integer, default=0)
    caterer = DB.Column(DB.Integer, DB.ForeignKey('caterers.id'))

    def __init__(self, name, price):
        self.name = name
        self.price = price
        # self.point = point

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
        except:
            return False
        else:
            self.caterer = caterer_id
            DB.session.add(self)

        return self.commit_changes()

    def update_meal(self, caterer, value):
        caterer = Caterer.get_caterer(username=None, caterer_id=caterer.id)
        if caterer:
            if isinstance(value, str):
                self.name = value
                return self.commit_changes()
            if isinstance(value, int):
                self.price = value
                return self.commit_changes()
        return False

    def get_meal(self):
        pass

    def get_meals(self):
        