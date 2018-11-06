from app import rest_api
from app.api.endpoints import OrderCollection, OrderItem

orders_namespace = rest_api.namespace('', description='Operations related to orders')

orders_namespace.route('/')(OrderCollection)
orders_namespace.route('/<string:uuid>')(OrderItem)
