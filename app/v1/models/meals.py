class DbMeals:
    """
    This class stores information about the meals offered by registered caterers.
    """
    def __init__(self):
        self.meals = dict()
        self.meal_id = 1

    def add_meal(self, caterer, meal_name, price):
        caterer_meals = self.meals.get(caterer, False)

        if not caterer_meals:
            meals = list()
            meal_id = self.meal_id
            easy_point = 0
            meal = [meal_id, meal_name, price, easy_point, caterer]
            meals.append(meal)

            self.meals[caterer] = meals
            self.meal_id += 1
            return True

        else:
            all_meals = self.meals[caterer]
            meal_id = self.meal_id
            # meal_id = all_meals[-1][0] + 1
            easy_point = 0
            all_meals.append([meal_id, meal_name, price, easy_point, caterer])
            self.meal_id += 1
            return True

        # for any reason meal not added
        return False

    def get_meal(self, caterer, meal_id):
        all_meals_caterer = self.get_all_meals(caterer)
        if not all_meals_caterer:
            return False
        else:
            length = len(all_meals_caterer)

        if isinstance(meal_id, int) and meal_id > 0:
            actual_id = meal_id -1
        else:
            return False

        if actual_id <= length:
            meal = all_meals_caterer[meal_id - 1]
            return meal

        return False

    def update_meal(self, caterer, meal_id, field_to_update, new_value):
        meal = self.get_meal(caterer, meal_id)
        if meal:
            if field_to_update == 'name':
                if isinstance(new_value, str):
                    meal[1] = new_value
            elif field_to_update == 'price':
                meal[2] = new_value
            self.get_all_meals(caterer)[meal_id-1] = meal
            return meal
        return False

    def get_all_meals(self, caterer):
        meals = self.meals.get(caterer, False)
        return meals

    def delete_meal(self, caterer, meal_id):
        deleted = False
        all_meals = self.get_all_meals(caterer)

        if all_meals:
            counter = 0
            list_length = len(all_meals)

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

    def easy_point(self, meal_id):
        all_meals = self.meals

        for meals in all_meals.values():
            for meal in meals:
                if meal[0] == meal_id:
                    meal[3] += 1
                    return True
        return False

