from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError
from app.v1.models.meal import Meal
from app.v1.models.caterer import Caterer


class Menu(DB.Model):
    """
        This class stores information about the menu of the day created by registered caterers.
    """
    __tablename__ = 'menus'
    id = DB.Column(DB.Integer, primary_key=True)
    meal = DB.Column(DB.Integer, DB.ForeignKey('meals.id'))
    order = DB.relationship('Order', backref='order')
    caterer = DB.Column(DB.Integer)

    def __init__(self, caterer_id, meal_id):
        self.caterer = caterer_id
        self.meal = meal_id

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            return False

    def add_meal_to_menu(self):
        meal = Meal.query.filter_by(id=self.meal).first()
        if not meal:
            return False

        if Menu.query.filter_by(caterer=self.caterer, meal=meal.id).first():
            return False

        if meal.caterer == self.caterer:
            DB.session.add(self)
            return Menu.commit_changes()
        return False

    @staticmethod
    def remove_meal_from_menu(caterer_id, meal_id):
        meal = Menu.query.filter_by(meal=meal_id).first()
        if not meal:
            return False
        if meal.caterer == caterer_id:
            DB.session.delete(meal)
            return Menu.commit_changes()
        return False

    @staticmethod
    def create_menu(caterer_id, *meal_ids):
        added_meals = []
        Menu.delete_menu(caterer_id=caterer_id)
        if not Caterer.query.filter_by(id=caterer_id).first():
            return False

        for meal_id in meal_ids:
            meal_added = Menu(caterer_id=caterer_id, meal_id=meal_id).add_meal_to_menu()

            if meal_added:
                added_meals.append(meal_id)

        if added_meals:
            return added_meals
        return False

    @staticmethod
    def delete_menu(caterer_id):
        menu = Menu.query.filter_by(caterer=caterer_id).all()
        print('menu_object', menu)
        print('all_menu_objects', Menu.query.all())
        if not menu:
            return False
        for menu_item in menu:
            DB.session.delete(menu_item)
        return Menu.commit_changes()

    @staticmethod
    def get_menu(caterer_id):
        menu = []
        raw_menu = Menu.query.filter_by(caterer=caterer_id)

        if not raw_menu:
            return False
        for menu_item in raw_menu:
            menu.append(
                dict(name=menu_item.menu.name, price=menu_item.menu.price, point=menu_item.menu.point,
                     caterer_id=menu_item.menu.caterer, menu_id=menu_item.id, meal_id=menu_item.menu.id,
                     brand_name=menu_item.menu.meal.brand_name)
            )

        return menu

    @staticmethod
    def get_menus():
        all_menus = {}
        raw_menus = Menu.query.all()

        for menu_item in raw_menus:
            if menu_item.menu.caterer not in all_menus.keys():
                all_menus[menu_item.menu.caterer] = Menu.get_menu(caterer_id=menu_item.caterer)

        if all_menus:
            return all_menus
        return False

    def __repr__(self):
        return 'Menu Object'

