from app.v1.models.users import DbUsers


class DbCaterers:
    """
    This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
    wont be inserted into the data structure.
    """
    def __init__(self):
        self.all_caterers = dict()
        self.all_emails = list()
        self.id = 1

    def add_caterer(self, email, username, password, address, category='caterer', brand_name=''):
        if email not in self.all_emails:
            caterer_exists = self.all_caterers.get(username, False)

            if not caterer_exists:
                brand_name_final = brand_name if brand_name else username
                self.all_caterers[username] = dict(email=email, username=username, password=password, address=address,
                                                   category=category, brand_name=brand_name_final)
                self.all_emails.append(email)
                return True

        return False

    def get_caterer(self, username):
        caterer = self.all_caterers.get(username, False)
        return caterer

    def get_all_caterers(self):
        return self.all_caterers

    def remove_caterer(self, username):
        caterer = self.all_caterers.get(username, False)
        if caterer:
            del self.all_caterers[username]
            return True
        return False

