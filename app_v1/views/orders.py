
from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
from app_v1.models.models import DbOrders

orders_db = DbOrders()

orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route('/orders', methods=['POST'])
@swag_from('api_doc/create_order.yml')
def create_order():
    data = request.get_json()
    try:
        if data['caterer'] and data['meal']:
            new_order = orders_db.add_order(customer='default', caterer=data['caterer'], meal=data['meal'])

            if new_order:
                message = 'Order {} successfully placed.'.format(data)
                return make_response(jsonify(message=message), 201)

    except KeyError:
        pass
    return make_response(jsonify(message='Invalid request format'), 403)


@orders.route('/orders/<int:meal_id>', methods=['PUT'])
@swag_from('api_doc/modify_order.yml')
def modify_order(meal_id):
    data = request.get_json()
    try:
        print('caterer', data['caterer'])
        print('meal', data['meal'])
        print('order list', orders_db.orders_caterers)
        if data['caterer'] and data['meal']:

            new_order = orders_db.modify_order(customer='default', caterer=data['caterer'], order_id=meal_id,
                                               meal=data['meal'])
            print('if start')
            print('new order', new_order)
            if new_order:
                print('inside if')
                message = 'Order {} successfully modified.'.format(data)
                return make_response(jsonify(message=message), 201)
            else:
                return make_response(jsonify(message="Resource not found"), 201)

    except KeyError:
        pass
    return make_response(jsonify(message='Invalid request format'), 403)


@orders.route('/orders', methods=['GET'])
@swag_from("api_doc/get_all_orders.yml")
def get_all_orders():
    orders_per_caterer = orders_db.get_orders(caterer='default10')
    if orders_per_caterer:
        message = 'The request was successfull'
        return make_response(jsonify(message=message, content=orders_per_caterer), 200)
    return make_response(jsonify(message='Oops, orders not found.'), 200)


@orders.route('/orders/clear/<int:order_id>', methods=['PUT'])
def clear_orders(order_id):
    pass


@orders.route('/orders/history', methods=['GET'])
def get_history():
    pass