from app.v1.models.db_connection import DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class User_info(DB.Model):
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
        if isinstance(user_object, User_info):
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
            user = User_info.query.filter_by(email=email).first()

        else:
            user = User_info.query.filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User_info.query.filter_by(user_id=user_id).first()
        try:
            DB.session.delete(user)
        except UnmappedInstanceError:
            return False
        else:
            return User_info.commit_changes()

    @staticmethod
    def get_users():
        return User_info.query.all()

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
            User_info.delete_user(user.customer.user_id)
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

        user_info = User_info.query.filter_by(email=self.email).first()
        print('user', user_info)
        if user_info:
            user_info.user_counter += 1
            self.user = user_info.user_id
            return self.save()
        else:
            new_user_info = User_info(email=self.email, first_name=self.first_name, last_name=self.last_name,
                                      address=self.address).add_user()
            if new_user_info:
                self.user = User_info.query.filter_by(email=self.email).first().user_id
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
            User_info.delete_user(caterer.caterer.user_id)
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

        user_info = User_info.query.filter_by(email=self.email).first()
        print('user', user_info)
        if user_info:
            user_info.user_counter += 1
            self.user = user_info.user_id
            return self.save()
        else:
            new_user_info = User_info(email=self.email, first_name=self.first_name, last_name=self.last_name,
                                      address=self.address).add_user()
            if new_user_info:
                self.user = User_info.query.filter_by(email=self.email).first().user_id
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