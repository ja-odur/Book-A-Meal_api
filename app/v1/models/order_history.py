from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError
from app.v1.models.meal import  Meal
import datetime


class OrderHistory(DB.Model):
    """
    This class stores information about the orders made by registered users. Allows users to modify their orders
    if it's still within the one hour time lap. This orders information is stored in a two forms that are
    easily accessible by users (to view their orders) and caterers ( to view all the orders placed with them).
    """
    __tablename__ = 'orderHistory'

    id = DB.Column(DB.Integer, primary_key=True)
    order_id = DB.Column(DB.Integer)
    meal = DB.Column(DB.String)
    price = DB.Column(DB.String)
    customer_id = DB.Column(DB.Integer)
    meal_id = DB.Column(DB.Integer)
    points = DB.Column(DB.Integer)
    customer = DB.Column(DB.String)
    caterer = DB.Column(DB.String)
    order_cleared = DB.Column(DB.Boolean)

    def __init__(self, order_id, meal, price, customer_id, meal_id, caterer, points, customer, order_cleared=True):
        self.order_id = order_id
        self.meal = meal
        self.price = price
        self.customer_id = customer_id
        self.meal_id = meal_id
        self.points = points
        self.customer = customer
        self.order_cleared = order_cleared
        self.caterer = caterer

    @staticmethod
    def commit_changes():
        try:
            DB.session.commit()
        except (IntegrityError, UnmappedInstanceError):
            DB.session.rollback()
            commit = False
        else:
            commit = True
        return commit

    def add_order_history(self):
        self.clear_time = datetime.datetime.now()
        DB.session.add(self)
        return OrderHistory.commit_changes()

    @staticmethod
    def get_order_history(customer_id):
        orders = OrderHistory.query.filter_by(customer_id=customer_id)

        if not orders:
            return False
        order_history = []

        for order in orders:
            meal = Meal.get_meal(order.meal_id)
            if meal:
                order.points = meal.point
            order_history.append(order.to_dictionary())
        return order_history

    def to_dictionary(self):
        return dict(order_id=self.order_id, meal=self.meal, price=self.price,
                    order_cleared=self.order_cleared, customer_id=self.customer_id, meal_id=self.meal_id,
                    caterer=self.caterer, points=self.points, customer=self.customer)