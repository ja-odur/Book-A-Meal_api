from app.v1.models.users import DbUsers


class DbCaterers(DbUsers):
    """
    This class stores information about the registered caterers. The username and email fields are unique and any duplicate value
    wont be inserted into the data structure.
    """
    def add_user(self, email, username, password, address, category='caterer', brand_name=''):
        if email not in self.all_emails:
            caterer_exists = self.all_users.get(username, False)

            if not caterer_exists and category=='caterer':
                brand_name_final = brand_name if brand_name else username
                self.all_users[username] = dict(email=email, username=username, password=password, address=address,
                                                category=category, brand_name=brand_name_final)
                self.all_emails.append(email)
                return True

        return False


