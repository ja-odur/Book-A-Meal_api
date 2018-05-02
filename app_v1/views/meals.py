from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from

from app_v1.models.models import DbMeals

meals_db = DbMeals()

meals = Blueprint('meals', __name__, url_prefix='/api/v1')


@meals.route('/meals/', methods=['POST'])
@swag_from('api_doc/create_meals.yml')
def create_meal():
    data = request.get_json()

    if meals_db.add_meal(data['username'], data['name'], data['price']):
        message = 'Meal {} successfully added.'.format(data['name'])
        return make_response(jsonify(dict(message=message)), 201)
    else:
        return make_response(jsonify(dict(message='meal not added.')), 401)


@meals.route('/meals/', methods=["GET"])
@swag_from('api_doc/get_all_meals.yml')
def get_all_meals():
    meals_per_caterer = meals_db.get_all_meals(caterer='default')
    if meals_per_caterer:
        return make_response(jsonify(message=meals_per_caterer), 201)
    return make_response(jsonify(message='Resource not found'), 404)


@meals.route('/meals/<int:meal_id>', methods=['PUT'])
@swag_from('api_doc/update_meal.yml')
def update_meal(meal_id):
    data = request.get_json()
    update, message = False, ''
    try:
        if data['name']:
            updated = meals_db.update_meal(caterer='default', meal_id=meal_id, update_field='name', value=data['name'])
    except KeyError:
        if data['price']:
            updated = meals_db.update_meal(caterer='default', meal_id=meal_id, update_field='price', value=data['price'])

    if updated:
        return make_response(jsonify(message=updated), 201)
    return make_response(jsonify(message='failed'), 201)


@meals.route('/meals/<int:meal_id>', methods=['DELETE'])
@swag_from('api_doc/delete_meal.yml')
def delete_meal(meal_id):
    meal_deleted = meals_db.delete_meal(caterer='default', meal_id=meal_id)

    if meal_deleted:
        return make_response(jsonify(message='meal deleted'), 201)
    return make_response(jsonify(message='deletion failed'), 404)
