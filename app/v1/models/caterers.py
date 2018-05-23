from app.v1.models.users import DbUsers


class DbCaterers:
    """
    This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
    wont be inserted into the data structure.
    """
    def __init__(self, users):
        self.caterers = {}
        self.id = 1
        self.users = users

    def add_caterer_by_id(self, user_id):
        new_caterer = self.users.get_user_by_id(user_id)
        if new_caterer:
            self.caterers[self.id] = user_id
            self.id += 1
            return True
        return False

    def add_caterer(self, email, username, password, address):
        user = self.users.get_user(username)
        new_caterer = False
        if not user:
            new_caterer = self.users.add_user(email, username, password, address)
        else:
            id_user = user['user_id']
            user = self.get_caterer_by_id(id_user)
            if not user:
                new_caterer = True
            else:
                new_caterer = False

        if new_caterer:
            user_id = self.users.get_user(username)['user_id']
            self.caterers[self.id] = user_id
            self.id += 1
            return True

        return False

    def get_caterer_by_id(self, caterer_id):
        if caterer_id not in self.caterers.keys():
            return False
        caterer = self.users.get_user_by_id(caterer_id)
        return caterer

    def get_caterer(self, username):
        user_info = self.users.get_user(username)
        if user_info:
            user_id = self.users.get_user(username)['user_id']

            user = self.get_caterer_by_id(user_id)
            return user
        return False
       


