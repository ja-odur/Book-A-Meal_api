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
    orders_per_caterer = orders_db.get_all_orders(caterer=caterer)
    if orders_per_caterer:
        message = 'The request was successfull'
        return make_response(jsonify(message=message, content=orders_per_caterer), 200)
    return make_response(jsonify(message='Oops, orders not found.'), 404)


@orders.route('/orders/placed', methods=['GET'])
@swag_from("api_doc/get_orders.yml")
@token_required()
def get_orders(current_user):
    """
    This function enables a user  to get all the orders that is already placed.
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns the orders if the operation is successful
    """
    customer = current_user[1]
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='This method is meant for customers only')), 403)

    placed_orders = orders_db.get_orders_per_user(customer)

    if placed_orders:
        return make_response(jsonify(dict(message=placed_orders)), 200)

    return make_response(jsonify(dict(message='No orders placed')), 200)


@orders.route('/orders/<int:order_id>', methods=['DELETE'])
@swag_from("api_doc/delete_order.yml")
@token_required()
def delete_order(current_user, order_id):
    """
    This function enables a user to delete a placed order
    :param current_user: A list containing the current users information i.e category username, email
    :param order_id: the id of the order to be deleted
    :return: returns a confirmation message
    """
    customer = current_user[1]
    if current_user[0] == 'caterer':
        return make_response(jsonify(dict(message='This method is meant for customers only')), 403)
    order_deleted = orders_db.delete_order(customer=customer, order_id=order_id)

    if order_deleted:
        return make_response(jsonify(dict(message='Order successfully deleted')), 201)
    return make_response(jsonify(dict(message='Order not found')), 404)


@orders.route('/orders/clear/<int:order_id>', methods=['PATCH'])
@token_required(admin=True)
@swag_from("api_doc/clear_order.yml")
def clear_order(current_user, order_id):
    """
    This function enable caterers to clear orders placed by users
    :param current_user: A list containing the current users information i.e category username, email
    :param order_id: the id of the order to be cleared
    :return: returns a confirmation message
    """
    caterer = current_user[1]
    cleared = orders_db.clear_order(caterer, order_id)

    if cleared:
        return make_response(jsonify(dict(message='Order successfully cleared')), 200)
    return make_response(jsonify(dict(message='Order does not exist')), 200)


@orders.route('/orders/history', methods=['GET'])
@swag_from("api_doc/order_history.yml")
@token_required()
def get_history(current_user):
    """
    This function enables users to get a list of previously cleared orders
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns the order history if the operation is successful
    """
    customer = current_user[1]
    category = current_user[0]

    if category == 'caterer':
        return make_response(jsonify(dict(message='Sorry operation not permitted for this user.')), 403)

    order_history = orders_db.get_order_history(customer=customer)

    if order_history:
        return make_response(jsonify(dict(message=order_history)), 200)
    return make_response(jsonify(dict(message='No order history')), 200)
