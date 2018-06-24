# from app.v1.models.db_connection import DB
#
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm.exc import UnmappedInstanceError
from app.v1.models.models import DB, UserInfo, IntegrityError, UnmappedInstanceError


class DbUsers:
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the data structure.
    """
    
    def __init__(self):
        self.all_users = dict()
        self.id = 1

    def add_user(self, email, username, password, address):
        for user_key in self.all_users.keys():
            existing_email = self.all_users[user_key]['email']
            if existing_email == email:
                return False

        if not self.all_users.get(username, False):
            self.all_users[username] = dict(email=email, username=username, password=password,
                                            address=address, user_id=self.id)
            self.id += 1
            return self.all_users[username]['user_id']
        return False

    def get_user(self, user_id):
        for user in self.all_users.values():
            if user['user_id'] == user_id:
                return user
        return False

    def get_users(self):
        return self.all_users

    def delete_user(self, username):
        user = self.all_users.get(username, False)
        if user:
            del self.all_users[username]
            return True
        return False


# class User(DB.Model):
#     """
#     This class stores information about the registered users
#     The username and email fields are unique and any duplicate value wont be inserted into
#     the database.
#     """
#     __tablename__ = 'users'
#     id = DB.Column(DB.Integer, primary_key=True)
#     username = DB.Column(DB.String(60), unique=True)
#     email = DB.Column(DB.String(160), unique=True)
#     password = DB.Column(DB.String(254), nullable=False)
#     user = DB.Column(DB.Integer, DB.ForeignKey('users_info.user_id'))
#     # caterer = DB.relationship('Caterer', backref='user')
#
#     def __init__(self, first_name, last_name, email, username, password, address='No address provided'):
#         self.email = email
#         self.username = username
#         self.password = password
#         self.address = address
#
#     @staticmethod
#     def to_dictionary(user_object):
#         if isinstance(user_object, User):
#             return dict(username=user_object.username, email=user_object.email, address=user_object.address,
#                         id=user_object.id)
#         return False
#
#     @staticmethod
#     def commit_changes():
#         try:
#             DB.session.commit()
#             return True
#         except (IntegrityError, UnmappedInstanceError):
#             DB.session.rollback()
#             return False
#
#     @staticmethod
#     def get_user(username, email=None, user_id=None):
#         if user_id:
#             user = User.query.filter_by(id=user_id).first()
#
#         elif email:
#             user = User.query.filter_by(email=email).first()
#         else:
#             user = User.query.filter_by(username=username).first()
#         return user
#         # return User.to_dictionary(user)
#
#     @staticmethod
#     def delete_user(username):
#         user = User.query.filter_by(username=username).first()
#         counter = user.user_id.user_counter
#         if counter <= 1:
#             User_info.delete_user(user.user_id)
#         try:
#             DB.session.delete(user)
#         except UnmappedInstanceError:
#             return False
#         else:
#             return User.commit_changes()
#
#     @staticmethod
#     def get_users():
#         return User.query.all()
#
#     def add_user(self):
#         user = DB.session.add(self)
#         print(user)
#         if self.commit_changes():
#             return True
#         return False


# class Caterer(DB.Model):
#     """
#     This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
#     wont be inserted into the database.
#     """
#
#     __tablename__ = 'caterers'
#     caterer_id = DB.Column(DB.Integer, primary_key=True)
#     brand_name = DB.Column(DB.String(120), nullable=True)
#     user_id = DB.Column(DB.Integer, DB.ForeignKey('users.user_id'))
#
#     def __init__(self):
#         self.brand_name = None
#
#     def add_caterer(self, email, username, password, address='', brand_name=''):
#         user = User.get_user(username=username, email=email)
#         if not user:
#             user = User(email=email, username=username, password=password, address=address).add_user()
#
#         if user:
#             self.brand_name = brand_name
#             self.user_id = User.get_user(username=username, email=email).user_id
#             DB.session.add(self)
#             DB.session.commit()
#             return True
#         return False
#
#     @staticmethod
#     def get_caterer(caterer_id):
#         return Caterer.query.filter_by(caterer_id=caterer_id).first()
#
#     @staticmethod
#     def get_caterers():
#         all_caterers = {}
#         caterers = Caterer.query.all()
#         for caterer in caterers:
#             user = User.get_user(username=None, user_id=caterer.user_id)
#             all_caterers[caterer.caterer_id] = [user.username, user.email, user.address, caterer.brand_name]
#         return all_caterers
#
#     @staticmethod
#     def delete_caterer(caterer_id):
#         caterer = Caterer.query.filter_by(caterer_id=caterer_id)
#         DB.session.delete(caterer)
#         DB.commit()






