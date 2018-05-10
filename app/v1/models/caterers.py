from app.v1.models.users import DbUsers

class DbCaterers(DbUsers):
    def __init__(self):
        super().__init__()

    def add_user(self, email, username, password, address, category='caterer', brand_name=''):
        if email not in self.all_emails:
            try:
                self.all_users[username]
            except KeyError:
                brand_name_final = brand_name if brand_name else username
                self.all_users[username] = dict(email=email, username=username, password=password, address=address,
                                                category=category, brand_name=brand_name_final)
                self.all_emails.append(email)
                return True

        return False