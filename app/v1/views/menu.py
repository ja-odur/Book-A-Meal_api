from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.decorators import token_required
from app.v1.models.models import Menu, Caterer


menu = Blueprint('menu', __name__, url_prefix='/api/v1')


@menu.route('/menu/', methods=['POST'])
@swag_from('api_doc/create_menu.yml')
@token_required(admin=True)
def create_menu(current_user):
    """
    This function enables caterers to create a daily menu
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a nested list of meal objects
    """
    caterer = Caterer.get_caterer(current_user[1])
    data = request.get_json()

    try:
        if not isinstance(data['meal_ids'], list):
            return make_response(jsonify(message='Please submit a list of meal ids.'), 400)
    except (KeyError, TypeError):
        return make_response(jsonify(message='Bad data format'), 400)

    if caterer:
        created_menu = Menu.create_menu(caterer.id, *data['meal_ids'])

        if created_menu:
            message = 'Menu successfully created.'
            return make_response(jsonify(message=message), 201)
    return make_response(jsonify(message='Menu not created.'), 400)


@menu.route('/menu/meals/add/', methods=['POST'])
@token_required(admin=True)
def add_meals_to_menu(current_user):
    """
       This function enables caterers to create a daily menu
       :param current_user: A list containing the current users information i.e category username, email
       :return: returns a nested list of meal objects
       """
    caterer = Caterer.get_caterer(current_user[1])
    data = request.get_json()

    try:
        if not isinstance(data['meal_ids'], list):
            return make_response(jsonify(message='Please submit a list of meal ids.'), 400)
    except (KeyError, TypeError):
        return make_response(jsonify(message='Bad data format'), 400)

    if caterer:
        created_list = []
        for meal_id in data['meal_ids']:
            result = Menu(caterer_id=caterer.id, meal_id=meal_id).add_meal_to_menu()
            created_list.append(result)

        if True in created_list:
            message = 'Menu successfully updated.'
            return make_response(jsonify(message=message), 201)
    return make_response(jsonify(message='Menu not created.'), 400)


@menu.route('/menu/meal/', methods=['POST'])
@token_required(admin=True)
def remove_meal_from_menu(current_user):
    """
       This function enables caterers to create a daily menu
       :param current_user: A list containing the current users information i.e category username, email
       :return: returns a nested list of meal objects
       """
    caterer = Caterer.get_caterer(current_user[1])
    data = request.get_json()
    print('data', data)

    try:
        if not data['meal_id']:
            return make_response(jsonify(message='Please submit a meal id.'), 400)
    except (KeyError, TypeError):
        return make_response(jsonify(message='Bad data format'), 400)

    if caterer:
        remove_meal = Menu.remove_meal_from_menu(caterer_id=caterer.id, meal_id=data['meal_id'])

        if remove_meal:
            message = 'Meal successfully removed.'
            return make_response(jsonify(message=message), 201)
    return make_response(jsonify(message='Meal Not removed.'), 400)


@menu.route('/menu/', methods=['GET'])
@swag_from('api_doc/get_menu.yml')
@token_required()
def get_menu(current_user):
    """
    This returns all the menus available from various caterers
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a dictionary mapping the caterer's name to their set daily menu
    """
    menu = Menu.get_menus()
    if menu:
        return make_response(jsonify(message=dict(MENU=menu)), 200)
    return make_response(jsonify(message='Menu not found.'), 404)


@menu.route('/caterer/menu/', methods=['GET'])
@token_required()
def get_menu_per_caterer(current_user):
    """
    This returns all the menus available from various caterers
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a dictionary mapping the caterer's name to their set daily menu
    """
    caterer = Caterer.get_caterer(current_user[1])

    menu = Menu.get_menu(caterer_id=caterer.id)
    if menu:
        return make_response(jsonify(message=dict(MENU=menu)), 200)
    return make_response(jsonify(message='Menu not found.'), 404)


@menu.route('/menu/meal/<int:meal_id>', methods=['DELETE'])
@token_required(admin=True)
def delete_meal_menu(current_user, meal_id):
    caterer = Caterer.get_caterer(username=current_user[1])
    removed_meal = Menu.remove_meal_from_menu(caterer_id=caterer.id, meal_id=meal_id)

    if removed_meal:
        return make_response(jsonify(message='Meal successfully removed from menu.'), 200)
    return make_response(jsonify(message='Meal not removed'), 404)


@menu.route('/menu/', methods=['DELETE'])
@token_required(admin=True)
def delete_menu(current_user):

    caterer = Caterer.get_caterer(username=current_user[1])

    if caterer:
        menu_deleted = Menu.delete_menu(caterer_id=caterer.id)

        if menu_deleted:
            return make_response(jsonify(message='Menu deleted'), 200)
    return make_response(jsonify(message='No menu found'), 404)







