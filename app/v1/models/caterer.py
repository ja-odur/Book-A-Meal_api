from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError, DataError
from app.v1.models.general_users_info import UserInfo


class Caterer(DB.Model):
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the database.
    """
    __tablename__ = 'caterers'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(60), unique=True)
    brand_name = DB.Column(DB.String(60), unique=True)
    email = DB.Column(DB.String(160), unique=True)
    password = DB.Column(DB.String(254), nullable=False)
    user = DB.Column(DB.Integer, DB.ForeignKey('users_info.user_id'))
    meal = DB.relationship('Meal', backref='meal')

    def __init__(self, caterer_data=dict(first_name=None, last_name=None, email=None, username=None, password=None,
                                         brand_name=None, address='No address provided')):
        self.email = caterer_data['email']
        self.username = caterer_data['username']
        self.brand_name = caterer_data['brand_name']
        self.password = caterer_data['password']
        self.address = caterer_data['address']
        self.first_name = caterer_data['first_name']
        self.last_name = caterer_data['last_name']

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            commit_status = True
        except (IntegrityError, UnmappedInstanceError, DataError):
            DB.session.rollback()
            commit_status = False
        return commit_status

    @staticmethod
    def get_caterer(username, email=None, caterer_id=None):
        return Caterer.query.filter_by(id=caterer_id).first() or Caterer.query.filter_by(email=email).first() or \
               Caterer.query.filter_by(username=username).first() or False

    @staticmethod
    def delete_caterer(username):
        caterer = Caterer.query.filter_by(username=username).first()
        if caterer:
            counter = caterer.caterer.user_counter
            if counter <= 1:
                UserInfo.delete_user(caterer.caterer.user_id)
            else:
                caterer.caterer.user_counter -= 1
                DB.session.commit()

            DB.session.delete(caterer)
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
