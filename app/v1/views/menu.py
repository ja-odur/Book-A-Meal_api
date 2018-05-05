from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.decorators import token_required
from app.v1.models.menu import DbMenu


menu_db = DbMenu()

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
    caterer = current_user[1]
    data = request.get_json()
    created_menu = menu_db.create_menu(caterer=caterer, daily_menu=data['menu'])

    if created_menu:
        message = 'Menu {} successfully added.'.format(data['menu'])
        return make_response(jsonify(message=message), 201)
    return make_response(jsonify(message='Bad data format'), 403)


@menu.route('/menu/', methods=['GET'])
@swag_from('api_doc/get_menu.yml')
@token_required()
def get_menu(current_user):
    """
    This returns all the menus available from various caterers
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a dictionary mapping the caterer's name to their set daily menu
    """
    menu = menu_db.get_menu()
    message = 'Todays menus, {}.'.format(menu)
    return make_response(jsonify(message=message), 200)

