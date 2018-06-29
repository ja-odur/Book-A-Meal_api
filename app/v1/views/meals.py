from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint

from app.v1.views.decorators import token_required
# from app.v1.models.meals import DbMeals
from app.v1.models.models import Caterer, Meal

# meals_db = DbMeals()

meals = Blueprint('meals', __name__, url_prefix='/api/v1')


@meals.route('/meals/', methods=['POST'])
@swag_from('api_doc/create_meals.yml')
@token_required(admin=True)
def create_meal(current_user):
    """
    This method creates enables a caterer to create a new meal.
    :param current_user: A list containing the current users information i.e category username, email
    """
    data = request.get_json()
    # username = current_user[1]
    caterer = Caterer.get_caterer(current_user[1])
    if caterer:
        if Meal(name=data['name'], price=data['price']).add_meal(caterer=caterer):
            message = 'Meal {} successfully added.'.format(data['name'])
            return make_response(jsonify(dict(message=message)), 201)

    return make_response(jsonify(dict(message='meal not added.')), 401)


@meals.route('/meals/', methods=["GET"])
@swag_from('api_doc/get_all_meals.yml')
@token_required(admin=True)
def get_all_meals(current_user):
    """
    This function enables a caterer to get all meals created for purposes of creating a menu
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a list containing all available meals
    """
    caterer = Caterer.get_caterer(current_user[1])
    meals_per_caterer = Meal.get_meals(caterer=caterer)
    if meals_per_caterer:
        return make_response(jsonify(message=meals_per_caterer), 201)
    return make_response(jsonify(message='Resource not found'), 404)


@meals.route('/meals/<int:meal_id>', methods=['PUT'])
@swag_from('api_doc/update_meal.yml')
@token_required(admin=True)
def update_meal(current_user, meal_id):
    """
    This function enables a caterer to update to modify a single attribute of the meal identified by its meal_id
    :param current_user: A list containing the current users information i.e category username, email
    :param meal_id: An integer used to identify the particular meal
    :return: returns a confirmation message i.e if successful of not
    """
    data = request.get_json()
    caterer = Caterer.get_caterer(current_user[1])

    updated, message = False, ''

    if not ('name' in data or 'price' in data):
        return make_response(jsonify({'message': 'Invalid data format'}), 403)

    if 'name' in data:
        updated = Meal.update_meal(caterer=caterer, meal_id=meal_id, value=data['name'])

    if 'price' in data:
        updated = Meal.update_meal(caterer=caterer, meal_id=meal_id, value=data['price'])

    if updated:
        return make_response(jsonify(message=updated), 201)
    return make_response(jsonify(message='failed'), 201)


@meals.route('/meals/<int:meal_id>', methods=['DELETE'])
@swag_from('api_doc/delete_meal.yml')
@token_required(admin=True)
def delete_meal(current_user, meal_id):
    """
    This function enables caterer to delete a created meal
    :param current_user: A list containing the current user's information i.e category username, email
    :param meal_id: n integer used to identify the particular meal
    :return: returns a confirmation message, whether successful or not.
    """
    caterer = current_user[1]
    meal_deleted = Meal.delete_meal(meal_id=meal_id)

    if meal_deleted:
        return make_response(jsonify(message='meal deleted'), 201)
    return make_response(jsonify(message='deletion failed, not item found to delete'), 404)


@meals.route('/meals/point/<int:meal_id>', methods=['POST'])
@swag_from('api_doc/easy_point.yml')
@token_required()
def easy_point(current_user, meal_id):
    """
    This function enables to point out best meals by giving the meal a point. Accumulated points
    are used to rank the meals
    :param current_user: A list containing the current user's information i.e category username, email
    :param meal_id: The id of the meal to pointed out
    :return: returns a confirmation message, whether the operation is successful or not.
    """
    category = current_user[0]
    if category == 'caterer':
        return make_response(jsonify(message='Operation not permitted for this user'), 403)

    point_out = Meal.easy_point(meal_id=meal_id)

    if point_out:
        return make_response(jsonify(message='Point out successful'), 200)
    return make_response(jsonify(message='Point out failed'), 200)
