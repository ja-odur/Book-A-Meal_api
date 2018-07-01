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



