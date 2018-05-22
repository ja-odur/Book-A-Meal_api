class DbMenu:
    """
        This class stores information about the menu of the day created by registered caterers.
        """
    def __init__(self):
        self.menu = dict()

    def create_menu(self, caterer, daily_menu):
        if isinstance(daily_menu, list):
            self.menu[caterer] = daily_menu
            return True

        return False

    def get_menu(self):
        return self.menu
