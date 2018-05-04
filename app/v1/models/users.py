class DbUsers:
    """
    This class stores information about the registered users
    The username and email fields are unique and any duplicate value wont be inserted into
    the data structure.
    """
    
    def __init__(self):
        self.all_users = dict()
        self.all_emails = list()
        self.id = 1

    def add_user(self, email, username, password, address):
        if email not in self.all_emails:
            try:
                self.all_users[username]
            except KeyError:
                self.all_users[username] = dict(email=email, username=username, password=password,
                                                address=address, id=self.id)
                self.all_emails.append(email)
                return True

            else:
                self.id +=1
                return False

        return False

    def get_user(self, username):
        try:
            return self.all_users[username]
        except KeyError:
            pass
        return False

    def get_all_users(self):
        return self.all_users

    def remove_user(self, username):
        try:
            del self.all_users[username]
        except KeyError:
            return False
        else:
            return True

