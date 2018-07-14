from flasgger import swag_from
from flask import jsonify, request, make_response, Blueprint
from app.v1.views.decorators import token_required
from app.v1.models.models import Order, User, Caterer
from app.v1.views.utils import block_caterer


orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route('/orders/<int:menu_id>', methods=['POST'])
@swag_from('api_doc/create_order.yml')
@token_required()
def create_order(current_user, menu_id):
    """
    This function enables only users to make an order
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns a confirmation message
    """
    # data = request.get_json()
    caterer_blocked = block_caterer(current_user=current_user, reason='Caterers can not create an order')
    if caterer_blocked:
        return caterer_blocked

    customer = User.get_user(current_user[1])

    if menu_id:
        new_order = Order(customer_id=customer.id, meal_id=menu_id).add_order()

        if new_order:
            message = 'Order successfully placed.'
            return make_response(jsonify(message=message), 201)

    return make_response(jsonify(message='Order not placed'), 404)


@orders.route('/orders/<int:order_id>', methods=['PUT'])
@swag_from('api_doc/modify_order.yml')
@token_required()
def modify_order(current_user, order_id):
    """
        This function enables only users to modify an order
        :param current_user: A list containing the current users information i.e category username, email
        :param order_id: the id of the order to be modified
        :return: returns a confirmation message
        """
    data = request.get_json()
    caterer_blocked = block_caterer(current_user=current_user, reason='Caterers can not modify an order')
    if caterer_blocked:
        return caterer_blocked
    try:
        meal_id = data['meal_id']
    except KeyError:
        return make_response(jsonify(message='Invalid request format'), 400)

    customer = User.get_user(current_user[1])

    updated_order = Order.modify_order(customer_id=customer.id, order_id=order_id, meal_id=meal_id)
    if updated_order:
        message = 'Order successfully modified.'
        return make_response(jsonify(message=message), 201)

    return make_response(jsonify(message="Resource not found"), 404)


@orders.route('/orders', methods=['GET'])
@swag_from("api_doc/get_all_orders.yml")
@token_required(admin=True)
def get_all_orders(current_user):
    """
    This function enables caterers to get all placed orders
    :param current_user: A list containing the current users information i.e category username, email
    :return: returns  confirmation message and the content containing all available orders.
    """
    caterer = Caterer.get_caterer(current_user[1])

    orders_per_caterer = Order.get_orders(caterer_id=caterer.id)
    if orders_per_caterer:
        return make_response(jsonify(message=dict(content=orders_per_caterer)), 200)
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
    customer = User.get_user(current_user[1])

    caterer_blocked = block_caterer(current_user=current_user, reason='This method is meant for customers only')
    if caterer_blocked:
        return caterer_blocked

    if customer:
        placed_orders = Order.get_orders(customer_id=customer.id)

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
    customer = User.get_user(current_user[1])

    caterer_blocked = block_caterer(current_user=current_user, reason='This method is meant for customers only')
    if caterer_blocked:
        return caterer_blocked

    order_deleted = Order.delete_order(customer_id=customer.id, order_id=order_id)

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
    caterer = Caterer.get_caterer(current_user[1])
    cleared = Order.clear_order(caterer_id=caterer.id, order_id=order_id)

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
    customer = User.get_user(current_user[1])

    caterer_blocked = block_caterer(current_user=current_user, reason='Sorry operation not permitted for caterers.')
    if caterer_blocked:
        return caterer_blocked

    order_history = Order.get_order_history(customer_id=customer.id)

    if order_history:
        return make_response(jsonify(dict(message=order_history)), 200)
    return make_response(jsonify(dict(message='No order history')), 200)
