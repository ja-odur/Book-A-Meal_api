from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint

from app.v1.views.decorators import token_required
from app.v1.models.models import DbMeals

meals_db = DbMeals()

meals = Blueprint('meals', __name__, url_prefix='/api/v1')


@meals.route('/meals/', methods=['POST'])
@swag_from('api_doc/create_meals.yml')
@token_required(admin=True)
def create_meal(current_user):
    data = request.get_json()
    username = current_user[1]
    if meals_db.add_meal(username, data['name'], data['price']):
        message = 'Meal {} successfully added.'.format(data['name'])
        return make_response(jsonify(dict(message=message)), 201)
    else:
        return make_response(jsonify(dict(message='meal not added.')), 401)


@meals.route('/meals/', methods=["GET"])
@swag_from('api_doc/get_all_meals.yml')
@token_required(admin=True)
def get_all_meals(current_user):
    caterer = current_user[1]
    meals_per_caterer = meals_db.get_all_meals(caterer=caterer)
    if meals_per_caterer:
        return make_response(jsonify(message=meals_per_caterer), 201)
    return make_response(jsonify(message='Resource not found'), 404)


@meals.route('/meals/<int:meal_id>', methods=['PUT'])
@swag_from('api_doc/update_meal.yml')
@token_required(admin=True)
def update_meal(current_user, meal_id):
    data = request.get_json()
    caterer = current_user[1]
    update, message = False, ''

    if not ('name' in data or 'price' in data):
        return make_response(jsonify({'message': 'Invalid data format'}), 403)

    try:
        if data['name']:
            updated = meals_db.update_meal(caterer=caterer, meal_id=meal_id, update_field='name', value=data['name'])
    except KeyError:
        if data['price']:
            updated = meals_db.update_meal(caterer=caterer, meal_id=meal_id, update_field='price', value=data['price'])

    if updated:
        return make_response(jsonify(message=updated), 201)
    return make_response(jsonify(message='failed'), 201)


@meals.route('/meals/<int:meal_id>', methods=['DELETE'])
@swag_from('api_doc/delete_meal.yml')
@token_required(admin=True)
def delete_meal(current_user, meal_id):
    caterer = current_user[1]
    meal_deleted = meals_db.delete_meal(caterer=caterer, meal_id=meal_id)

    if meal_deleted:
        return make_response(jsonify(message='meal deleted'), 201)
    return make_response(jsonify(message='deletion failed, not item found to delete'), 404)
