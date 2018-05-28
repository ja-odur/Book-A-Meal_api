class DbUsers:
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the data structure.
    """
    
    def __init__(self):
        self.all_users = dict()
        self.id = 1

    def add_user(self, email, username, password, address):
        all_emails = []
        for user_key in self.all_users.keys():
            existing_email = self.all_users[user_key]['email']
            all_emails.append(existing_email)

        if email not in all_emails:
            user_exists = self.all_users.get(username, False)

            if not user_exists:
                self.all_users[username] = dict(email=email, username=username, password=password,
                                                address=address, user_id=self.id)
                self.id += 1
                return True
        return False

    def get_user(self, user_id):
        all_users = self.all_users
        for user in all_users.values():
            if user['user_id'] == user_id:
                return user
        return False

    def get_users(self):
        return self.all_users

    def delete_user(self, username):
        user = self.all_users.get(username, False)
        if user:
            del self.all_users[username]
            return True
        return False
