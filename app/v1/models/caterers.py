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
        user_info = False
        users = self.users.get_users()

        for user in users.values():
            if user['username'] == username:
                user_info = user

        new_caterer = False
        if not user_info:
            new_caterer = self.users.add_user(email, username, password, address)
        else:
            if not user_info:
                new_caterer = True
            else:
                new_caterer = False

        if new_caterer:
            if user_info:
                user_id = user_info['user_id']
            else:
                users = self.users.get_users()
                for user in users.values():
                    if user['username'] == username:
                        info = user
                user_id = info['user_id']
            self.caterers[self.id] = user_id
            self.id += 1
            return True

        return False

    def get_caterer(self, caterer_id):
        if caterer_id not in self.caterers.keys():
            return False
        user_id_for_caterer = self.caterers[caterer_id]
        caterer = self.users.get_user(user_id_for_caterer)
        # caterer = self.users.get_user(caterer_id)
        print('Id caterer', caterer_id)
        print('Returned caterer', caterer)
        return caterer

    def get_all_caterers(self):
        print('All caterers', self.caterers)
        return self.caterers

    def delete_caterer(self, caterer_id):
        caterer = self.caterers.get(caterer_id, False)
        if caterer:
            del self.caterers[caterer_id]
            return True
        return False
       


