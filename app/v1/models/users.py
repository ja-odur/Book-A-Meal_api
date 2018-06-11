from app.v1.models.db_connection import DB
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

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


class User(DB.Model):
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the database.
    """
    __tablename__ = 'users'
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    username = DB.Column(DB.String(60), unique=True)
    password = DB.Column(DB.String(254), nullable=False)
    address = DB.Column(DB.String(254))
    user_id = DB.Column(DB.Integer, primary_key=True)

    def __init__(self, email, username, password, address='No address provided'):
        self.email = email
        self.username = username
        self.password = password
        self.address = address

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except IntegrityError:
            DB.session.rollback()
            return False

    def add_user(self):
        user = DB.session.add(self)
        print(user)
        if self.commit_changes():
            return True
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

