from app.v1.models.db_connection import DB, IntegrityError, UnmappedInstanceError
from app.v1.models.order_history import OrderHistory
import datetime


class Order(DB.Model):
    """
    This class stores information about the orders made by registered users. Allows users to modify their orders
    if it's still within the one hour time lap. This orders information is stored in a two forms that are
    easily accessible by users (to view their orders) and caterers ( to view all the orders placed with them).
    """
    __tablename__ = 'orders'

    id = DB.Column(DB.Integer, primary_key=True)
    meal = DB.Column(DB.Integer, DB.ForeignKey('menus.id'), nullable=False)
    order_time = DB.Column(DB.DateTime, nullable=False)
    order_cleared = DB.Column(DB.Boolean, default=False)
    customer = DB.Column(DB.Integer, DB.ForeignKey('users.id'))

    ORDER_MODIFICATION_EXPIRY = datetime.timedelta(hours=1).total_seconds()

    def __init__(self, customer_id, meal_id):
        self.customer = customer_id
        self.meal = meal_id

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

    def add_order(self):
        self.order_time = datetime.datetime.now()
        DB.session.add(self)
        return Order.commit_changes()

    @staticmethod
    def modify_order(customer_id, order_id, meal_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.customer != customer_id:
            return False

        elapsed_time = datetime.datetime.now() - order.order_time

        if elapsed_time.total_seconds() > Order.ORDER_MODIFICATION_EXPIRY:
            return False

        order.meal = meal_id
        return Order.commit_changes()

    @staticmethod
    def get_orders(customer_id=None, caterer_id=None):
        raw_orders = Order.query.filter_by(customer=customer_id)
        if customer_id and raw_orders:
            orders = []
            for order in raw_orders:
                if not caterer_id and not order.order_cleared:
                    orders.append(order.to_dictionary())
            return orders

        raw_orders = Order.query.all()

        if caterer_id and raw_orders:
            orders = []
            for order in raw_orders:
                if order.order.menu.caterer == caterer_id and not order.order_cleared:
                    orders.append(order.to_dictionary())
            return orders
        return False

    @staticmethod
    def delete_order(customer_id, order_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.customer != customer_id:
            return False

        elapsed_time = datetime.datetime.now() - order.order_time

        if elapsed_time.total_seconds() > Order.ORDER_MODIFICATION_EXPIRY:
            return False

        DB.session.delete(order)
        return Order.commit_changes()

    @staticmethod
    def clear_order(caterer_id, order_id):
        order = Order.query.filter_by(id=order_id).first()

        if not order:
            return False
        if order.order.menu.caterer == caterer_id:
            order.order_cleared = True
            order_history = order.to_dictionary()
            OrderHistory(**order_history).add_order_history()
            DB.session.delete(order)
            return Order.commit_changes()
        return False

    @staticmethod
    def get_order_history(customer_id):
        orders = OrderHistory.get_order_history(customer_id=customer_id)

        if not orders:
            return False
        order_history = []

        for order in orders:

            order_history.append(order)
        return order_history

    def to_dictionary(self):
        return dict(order_id=self.id, meal=self.order.menu.name, price=self.order.menu.price,
                    order_cleared=self.order_cleared, customer_id=self.customer, meal_id=self.order.menu.id,
                    caterer=self.order.menu.meal.brand_name, points=self.order.menu.point,
                    customer="{} {}".format(self.client.customer.first_name, self.client.customer.last_name))
