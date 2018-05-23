import datetime


class DbOrders:
    """
    This class stores information about the orders made by registered users. Allows users to modify their orders
    if it's still within the one hour time laps. This orders information is stored in a two forms that are
    easily accessible by users (to view their orders) and caterers ( to view all the orders placed with them).
    """
    def __init__(self):
        self.orders_customers = dict()
        self.orders_caterers = dict()
        self.orders_history = dict()
        self.order_expiry_time = datetime.timedelta(minutes=1).total_seconds()
        self.id_count = 1

    def add_order(self, customer, caterer, meal):
        order_time = datetime.datetime.now()
        order_customer_format = dict(order_id=self.id_count, meal=meal, caterer=caterer, cleared=False,
                                     order_time=order_time)
        order_caterer_format = dict(order_id=self.id_count, meal=meal, customer=customer, cleared=False
                                    , order_time=order_time)
        self.id_count += 1
        set_customer_order = False
        set_caterer_order = False

        orders_customers = self.orders_customers.get(customer, False)
        orders_caterers = self.orders_caterers.get(caterer, False)

        if not orders_customers:
            self.orders_customers[customer] = [order_customer_format]
            set_customer_order = True
        else:
            self.orders_customers[customer].append(order_customer_format)
            set_customer_order = True

        if not orders_caterers:
            self.orders_caterers[caterer] = [order_caterer_format]
            set_caterer_order = True
        else:
            self.orders_caterers[caterer].append(order_caterer_format)
            set_caterer_order = True

        if set_customer_order and set_caterer_order:
            return True
        return False

    def modify_order(self, customer, caterer, order_id, meal):
        time_now = datetime.datetime.now()
        orders = self.orders_customers.get(customer, False)
        orders_caterers = self.orders_caterers.get(caterer, False)

        if orders and orders_caterers:
            match_found = False
            matched_caterer_found = False
            counter_customer = 0
            counter_caterer = 0

            while counter_customer < len(orders):
                if orders[counter_customer]['order_id'] == order_id:
                    match_found = True
                    break
                counter_customer += 1

            while counter_caterer < len(orders_caterers):
                if orders_caterers[counter_caterer]['order_id'] == order_id and \
                        orders_caterers[counter_caterer]['customer'] == customer:
                    matched_caterer_found = True
                    break
                counter_caterer += 1

            if match_found and matched_caterer_found:
                order_time = self.orders_customers[customer][counter_customer]['order_time']
                elapse_time = time_now - order_time
                if elapse_time.total_seconds() <= self.order_expiry_time:
                    self.orders_customers[customer][counter_customer]['meal'] = meal
                    self.orders_caterers[caterer][counter_caterer]['meal'] = meal

                    return True
                else:
                    return False

        return False

    def get_orders(self, caterer):
        orders = self.orders_caterers.get(caterer, False)
        return orders

    def get_orders_per_user(self, user):
        orders = self.orders_customers.get(user, False)
        return orders

    def delete_order(self):
        pass

    def clear_order(self, caterer, customer, order_id):
        pass

    def get_order_history(self, customer):
        pass
