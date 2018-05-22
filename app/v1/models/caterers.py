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
        new_caterer = self.users.add_user(email, username, password, address)

        if new_caterer:
            user_id = self.users.get_user(username)['user_id']
            self.caterers[self.id] = user_id
            self.id += 1
            return True

        return False

    def get_caterer_by_id(self, id):
        caterer = self.users.get_user_by_id(id)
        return caterer

    def get_caterer(self, username):
        caterer = self.users.get_user(username)
        return caterer


