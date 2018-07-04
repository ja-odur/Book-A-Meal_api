from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError


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
