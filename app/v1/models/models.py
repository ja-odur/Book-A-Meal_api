import datetime
# =====================================DbUsers==============================================

class DbUsers:
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


class DbCaterers(DbUsers):
    def __init__(self):
        super().__init__()

    def add_user(self, email, username, password, address, category='caterer', brand_name=''):
        if email not in self.all_emails:
            try:
                self.all_users[username]
            except KeyError:
                brand_name_final = brand_name if brand_name else username
                self.all_users[username] = dict(email=email, username=username, password=password, address=address,
                                                category=category, brand_name=brand_name_final)
                self.all_emails.append(email)
                return True

        return False

# =======================================DbMeals=================================================

class DbMeals:
    def __init__(self):
        self.meals = dict()
        # self.id

    def add_meal(self, caterer, meal_name, price):
        try:
            self.meals[caterer]
        except KeyError:
            meals = list()
            meal_id = 1
            meal = [meal_id, meal_name, price]
            meals.append(meal)

            self.meals[caterer] = meals
            # self.id += 1
            return True

        else:
            all_meals = self.meals[caterer]
            meal_id = all_meals[-1][0] + 1
            all_meals.append([meal_id, meal_name, price])
            return True

        # for any reason meal not added
        return False

    def get_meal(self, caterer, meal_id):
        try:
            all_meals_caterer = self.get_all_meals(caterer)
            meal = all_meals_caterer[meal_id - 1]
        except (KeyError, IndexError):
            pass
        else:
            return meal
        return False

    def update_meal(self, caterer, meal_id, update_field, value):
        meal = self.get_meal(caterer, meal_id)
        if meal:
            if update_field == 'name':
                meal[1] = value
            elif update_field == 'price':
                meal[2] = value
            self.get_all_meals(caterer)[meal_id-1] = meal
            return meal
        return False

    def get_all_meals(self, caterer):
        try:
            if self.meals[caterer]:
                return self.meals[caterer]
        except KeyError:
            pass
        return False

    def delete_meal(self, caterer, meal_id):
        deleted = False
        all_meals = self.get_all_meals(caterer)

        if all_meals:
            counter, list_length = 0, len(all_meals)
            while counter < list_length:
                meal = all_meals[counter]

                if meal[0] == meal_id:
                    deleted = True
                    break

                counter += 1
            if deleted:
                del self.meals[caterer][counter]
                return True

        return False


# ============================================DbMenu===============================================

class DbMenu:
    def __init__(self):
        self.menu = dict()

    def create_menu(self, caterer, daily_menu):
        if isinstance(daily_menu, list):
            self.menu[caterer] = daily_menu
            return True
        return False

    def get_menu(self):
        return self.menu


# ===========================================DbOrders===============================

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






