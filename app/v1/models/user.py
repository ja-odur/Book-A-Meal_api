from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError
from app.v1.models.general_users_info import UserInfo


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

    def to_dictionary(self):
        return dict(username=self.username, email=self.email, address=self.address,
                    user_id=self.id)

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    @staticmethod
    def get_user(username=None, email=None, user_id=None):
        try:
            user = User.query.filter_by(email=email).first() or User.query.filter_by(id=user_id).first() or \
                   User.query.filter_by(username=username).first()

        except NameError:
            return False

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
        user = self.get_user(email=self.email) or self.get_user(username=self.username)
        if user:
            return False

        user_info = UserInfo.query.filter_by(email=self.email).first()

        if user_info:
            user_info.user_counter += 1
            self.user = user_info.user_id
            # return self.save()
        else:
            new_user_info = UserInfo(email=self.email, first_name=self.first_name, last_name=self.last_name,
                                     address=self.address).add_user()
            if new_user_info:
                self.user = UserInfo.query.filter_by(email=self.email).first().user_id
        return self.save()
        # return False

    def save(self):
        DB.session.add(self)
        return self.commit_changes()


