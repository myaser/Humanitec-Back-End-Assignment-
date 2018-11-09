from flask import request
from flask_jwt_simple import jwt_required
from flask_restplus import Resource, marshal

from app import rest_api
from app.api.parsers import authentication_parser, search_parser
from app.api.serializers import order, quantity
from app.repositories import OrderRepository


@rest_api.expect(authentication_parser)
class OrderCollection(Resource):

    @rest_api.marshal_list_with(order)
    @rest_api.expect(search_parser)
    @jwt_required
    def get(self):
        """
        Returns list of orders.
        """
        orders = OrderRepository.list_(conditions=request.args)
        return orders

    @rest_api.response(201, 'Order successfully created.')
    @rest_api.response(409, 'data integrity error.')
    @rest_api.expect(order, validate=True)
    @jwt_required
    def post(self):
        """
        Creates a new order.
        """
        data = marshal(request.json, order, skip_none=True)
        return OrderRepository.create(data), 201


@rest_api.response(404, 'Order not found.')
@rest_api.expect(authentication_parser)
class OrderItem(Resource):

    @rest_api.marshal_with(order)
    @jwt_required
    def get(self, uuid):
        """
        Returns a order
        """
        return OrderRepository.retrieve(uuid)

    @rest_api.expect(quantity, validate=True)
    @rest_api.response(204, 'Order successfully updated.')
    @jwt_required
    def patch(self, uuid):
        """
        Updates a order.
        Use this method to change the name of an Order.
        * Specify the UUID of the Order to modify in the request URL path.
        """
        data = marshal(request.json, quantity, skip_none=True)
        if data:
            OrderRepository.update(uuid, data)
        return None, 204

    @rest_api.response(204, 'Order successfully deleted.')
    @jwt_required
    def delete(self, uuid):
        """
        Deletes Order.
        """
        OrderRepository.delete(uuid)
        return None, 204
