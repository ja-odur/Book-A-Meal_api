import datetime

class DbOrders:
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

        try:
            self.orders_customers[customer]
        except KeyError:
            self.orders_customers[customer] = [order_customer_format]
            set_customer_order = True
        else:
            self.orders_customers[customer].append(order_customer_format)
            set_customer_order = True

        try:
            self.orders_caterers[caterer]
        except KeyError:
            self.orders_caterers[caterer] = [order_caterer_format]
            set_caterer_order = True
        else:
            self.orders_caterers[caterer].append(order_caterer_format)
            set_caterer_order = True

        if(set_customer_order and set_caterer_order):
            return True
        return False

    def modify_order(self, customer, caterer, order_id, meal):
        time_now = datetime.datetime.now()
        try:
            # print('in try block')
            orders = self.orders_customers[customer]
            orders_caterers = self.orders_caterers[caterer]
        except KeyError:
            pass
        else:
            # print('in try-except-else block')
            match_found = False
            matched_caterer_found = False
            counter_customer = 0
            counter_caterer = 0

            while counter_customer < len(orders):
                # print('in loop_customer')
                if orders[counter_customer]['order_id'] == order_id:
                    match_found = True
                    # print('found_customer')
                    break
                counter_customer += 1

            while counter_caterer < len(orders_caterers):
                # print('inloop_caterer')
                if orders_caterers[counter_caterer]['order_id'] == order_id and \
                        orders_caterers[counter_caterer]['customer'] == customer:
                    matched_caterer_found = True
                    # print('found_caterer')
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
                    # return 'elapsed time'

        # return 'end hit'
        return False


    def get_orders(self, caterer):
        try:
            return self.orders_caterers[caterer]
        except KeyError:
            return False

    def clear_order(self, caterer, customer, order_id):
        pass

    def get_order_history(self, customer):
        pass
