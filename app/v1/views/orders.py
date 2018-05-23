from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.decorators import token_required
from app.v1.models.orders import DbOrders

orders_db = DbOrders()

orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route('/orders', methods=['POST'])
@swag_from('api_doc/create_order.yml')
@token_required()
def create_order(current_user):
    """
    This function enables only users to make an order
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a confirmation message
    """
    data = request.get_json()
    customer = current_user[1]
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='Caterers can not create an order')), 403)
    try:
        if data['caterer'] and data['meal']:
            new_order = orders_db.add_order(customer=customer, caterer=data['caterer'], meal=data['meal'])

            if new_order:
                message = 'Order {} successfully placed.'.format(data)
                return make_response(jsonify(message=message), 201)

    except KeyError:
        return make_response(jsonify(message='Invalid request format'), 403)


@orders.route('/orders/<int:meal_id>', methods=['PUT'])
@swag_from('api_doc/modify_order.yml')
@token_required()
def modify_order(current_user, meal_id):
    """
        This function enables only users to modify an order
        :param current_user: A list containing the current users information i.e category username, email
        :return: returns a confirmation message
        """
    data = request.get_json()
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='Caterers can not modify an order')), 403)
    try:
        customer = current_user[1]
        if data['caterer'] and data['meal']:

            new_order = orders_db.modify_order(customer=customer, caterer=data['caterer'], order_id=meal_id,
                                               meal=data['meal'])
            if new_order:
                message = 'Order {} successfully modified.'.format(data)
                return make_response(jsonify(message=message), 201)
            else:
                return make_response(jsonify(message="Resource not found"), 201)

    except KeyError:
        return make_response(jsonify(message='Invalid request format'), 403)


@orders.route('/orders', methods=['GET'])
@swag_from("api_doc/get_all_orders.yml")
@token_required(admin=True)
def get_all_orders(current_user):
    """
    This function enables caterers to get all placed orders
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns  confirmation message and the content containing all available orders.
    """
    caterer = current_user[1]
    orders_per_caterer = orders_db.get_orders(caterer=caterer)
    if orders_per_caterer:
        message = 'The request was successfull'
        return make_response(jsonify(message=message, content=orders_per_caterer), 200)
    return make_response(jsonify(message='Oops, orders not found.'), 404)


@orders.route('/orders/placed', methods=['GET'])
@token_required()
def get_orders(current_user):
    customer = current_user[1]
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='This method is meant for customers only')), 403)

    placed_orders = orders_db.get_orders_per_user(customer)

    if placed_orders:
        return make_response(jsonify(dict(message=placed_orders)), 200)

    return make_response(jsonify(dict(message='No orders placed')), 200)


@orders.route('/orders/<int:order_id>', methods=['DELETE'])
@token_required()
def delete_order(current_user, order_id):
    customer = current_user[1]
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='This method is meant for customers only')), 403)
    order_deleted = orders_db.delete_order(customer=customer, order_id=order_id)

    if order_deleted:
        return make_response(jsonify(dict(message='Order successfully deleted')), 201)
    return make_response(jsonify(dict(message='Order not found')), 404)


@orders.route('/orders/clear/<int:order_id>', methods=['PUT'])
@token_required(admin=True)
def clear_orders(current_user, order_id):
    pass


@orders.route('/orders/history', methods=['GET'])
@token_required()
def get_history(current_user):
    pass


@orders.route('/orders/point', methods=['POST'])
@token_required()
def easy_point(current_user):
    pass
