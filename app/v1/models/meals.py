

class DbMeals:
    def __init__(self):
        self.meals = dict()

    def add_meal(self, caterer, meal_name, price):
        try:
            self.meals[caterer]
        except KeyError:
            meals = list()
            meal_id = 1
            meal = [meal_id, meal_name, price]
            meals.append(meal)

            self.meals[caterer] = meals
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
        except (KeyError, IndexError, TypeError):
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
