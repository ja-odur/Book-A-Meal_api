import datetime


class DbOrders:
    """
    This class stores information about the orders made by registered users. Allows users to modify their orders
    if it's still within the one hour time laps. This orders information is stored in a two forms that are
    easily accessible by users (to view their orders) and caterers ( to view all the orders placed with them).
    """
    def __init__(self):
        self.orders_customers = dict()
        self.order_expiry_time = datetime.timedelta(minutes=1).total_seconds()
        self.id_count = 1

    def add_order(self, customer, caterer, meal):
        order_time = datetime.datetime.now()
        order_customer_format = dict(order_id=self.id_count, meal=meal, caterer=caterer, cleared=False,
                                     order_time=order_time, customer=customer)

        self.id_count += 1
        set_customer_order = False

        orders_customers = self.orders_customers.get(customer, False)

        if not orders_customers:
            self.orders_customers[customer] = [order_customer_format]
            set_customer_order = True
        else:
            self.orders_customers[customer].append(order_customer_format)
            set_customer_order = True

        if set_customer_order:
            return True
        return False

    def modify_order(self, customer, caterer, order_id, meal):
        time_now = datetime.datetime.now()
        orders = self.orders_customers.get(customer, False)

        if orders:
            match_found = False
            counter_customer = 0

            while counter_customer < len(orders):
                if orders[counter_customer]['order_id'] == order_id:
                    match_found = True
                    break
                counter_customer += 1

            if match_found:
                order_time = self.orders_customers[customer][counter_customer]['order_time']
                elapse_time = time_now - order_time
                if elapse_time.total_seconds() <= self.order_expiry_time:
                    self.orders_customers[customer][counter_customer]['meal'] = meal

                    return True
                else:
                    return False

        return False

    def get_all_orders(self, caterer):
        all_orders = []
        for orders in self.orders_customers.values():
            for order in orders:
                if order['caterer'] == caterer:
                    all_orders.append(order)
        if all_orders:
            return all_orders
        return False

    def get_orders_per_user(self, user):
        orders = self.orders_customers.get(user, False)
        return orders

    def delete_order(self, customer, order_id):
        all_orders = self.orders_customers.get(customer, False)
        time_now = datetime.datetime.now()
        if all_orders:
            counter = 0
            for order in all_orders:
                if order['order_id'] == order_id and not order['cleared']:
                    order_time = order['order_time']
                    elapse_time = time_now - order_time
                    if elapse_time.total_seconds() <= self.order_expiry_time:
                        del all_orders[counter]
                        return True
                counter += 1
        return False

    def clear_order(self, caterer, order_id):
        orders_per_caterer = self.get_all_orders(caterer)
        if orders_per_caterer:
            for order in orders_per_caterer:
                if order['order_id'] == order_id and not order['cleared']:
                    order['cleared'] = True
                    return True
        return False

    def get_order_history(self, customer):
        orders = self.get_orders_per_user(customer)
        order_history = []
        for order in orders:
            if order['cleared']:
                order_history.append(order)
        if order_history:
            return order_history
        return False


