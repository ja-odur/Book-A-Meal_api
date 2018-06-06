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

       


