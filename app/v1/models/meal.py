from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError, DataError
from app.v1.models.caterer import Caterer


class Meal(DB.Model):
    """
        This class stores information about the meals offered by each registered caterer.
    """
    __tablename__ = 'meals'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120),nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
    point = DB.Column(DB.Integer, default=0)
    caterer = DB.Column(DB.Integer, DB.ForeignKey('caterers.id'))
    menu = DB.relationship('Menu', backref='menu')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
            return True
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
        except DataError:
            DB.session.rollback()
        return False

    def add_meal(self, caterer):
        try:
            caterer_id = caterer.id
            meal = Meal.query.filter_by(name=self.name).first()
        except AttributeError:
            return False
        else:
            if meal and (meal.caterer == caterer_id):
                return False
            self.caterer = caterer_id
            DB.session.add(self)

        return self.commit_changes()

    @staticmethod
    def update_meal(caterer, meal_id, value):
        caterer = Caterer.get_caterer(username=None, caterer_id=caterer.id)
        meal = Meal.get_meal(meal_id)
        if caterer:
            if meal and caterer.id == meal.caterer:
                if isinstance(value, str):
                    meal.name = value
                    return Meal.commit_changes()

                if isinstance(value, int):
                    meal.price = value
                    return Meal.commit_changes()
        return False

    @staticmethod
    def get_meal(meal_id):
        return Meal.query.filter_by(id=meal_id).first()

    @staticmethod
    def get_meals(caterer):
        meals = []
        try:
            raw_meals = Meal.query.filter_by(caterer=caterer.id)
        except AttributeError:
            return False

        if raw_meals:
            for meal in raw_meals:
                meals.append(meal.to_dictionary())
        return meals or False

    @staticmethod
    def delete_meal(meal_id):
        meal = Meal.query.filter_by(id=meal_id).first()
        if meal:
            DB.session.delete(meal)
            return Meal.commit_changes()
        return False

    @staticmethod
    def easy_point(meal_id):
        meal = Meal.query.filter_by(id=meal_id).first()

        if meal:
            meal.point += 1
            return Meal.commit_changes()
        return False

    def to_dictionary(self):
        return dict(name=self.name, price=self.price, point=self.point, caterer_id=self.caterer, meal_id=self.id,
                    caterer=self.meal.brand_name)

    @staticmethod
    def get_trending():
        raw_meals = Meal.query.all()
        meals = []
        for meal in raw_meals:
            meals.append(meal.to_dictionary())

        meals.sort(key=lambda m: m['point'], reverse=True)
        return meals

    def __repr__(self):
        return "Meal ->(name={}, price={})".format(self.name, self.price)
