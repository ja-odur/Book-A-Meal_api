# from app.v1.models.users import DbUsers
# from app.v1.models.db_connection import DB
from app.v1.models.users import User, DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class DbCaterers:
    """
    This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
    wont be inserted into the data structure.
    """
    def __init__(self, users):
        self.caterers = {}
        self.id = 1
        self.users = users

    def add_caterer(self, email, username, password, address):
        users = self.users.get_users()
        for user_key in self.caterers.values():
            if username == self.users.get_user(user_key)['username']:
                return False

        for user in users.values():
            if user['username'] == username:
                self.caterers[self.id] = user['user_id']
                self.id += 1
                return True

        self.caterers[self.id] = self.users.add_user(email, username, password, address)
        self.id += 1

        return True

    def get_caterer(self, caterer_id):
        if caterer_id not in self.caterers.keys():
            return False
        user_id_for_caterer = self.caterers[caterer_id]
        caterer = self.users.get_user(user_id_for_caterer)
        return caterer

    def get_caterers(self):
        all_caterers = {}

        for caterer_id in self.caterers.keys():
            all_caterers[caterer_id] = self.get_caterer(caterer_id)
        return all_caterers

    def delete_caterer(self, caterer_id):
        caterer = self.caterers.get(caterer_id, False)
        if caterer:
            del self.caterers[caterer_id]
            return True
        return False

#
# class Caterer(DB.Model):
#     """
#     This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
#     wont be inserted into the database.
#     """
#
#     __tablename__ = 'caterers'
#     caterer_id = DB.Column(DB.Integer, primary_key=True)
#     brand_name = DB.Column(DB.String(120), nullable=True)
#     user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
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
#             DB.session.add(self,user=user)
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
#
#


