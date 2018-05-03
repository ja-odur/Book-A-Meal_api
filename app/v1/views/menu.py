from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.decorators import token_required

from app.v1.models.models import DbMenu

menu_db = DbMenu()

menu = Blueprint('menu', __name__, url_prefix='/api/v1')


@menu.route('/menu/', methods=['POST'])
@swag_from('api_doc/create_menu.yml')
@token_required(admin=True)
def create_menu(current_user):
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
    menu = menu_db.get_menu()
    message = 'Todays menu {}.'.format(menu)
    return make_response(jsonify(message=message), 200)

