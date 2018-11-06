from flask import request
from flask_jwt_simple import jwt_required
from flask_restplus import Resource

from app import rest_api
from app.api.parsers import authentication_parser
from app.api.serializers import order
from app.repositories import OrderRepository


@rest_api.expect(authentication_parser)
class OrderCollection(Resource):

    @rest_api.marshal_list_with(order)
    @jwt_required
    def get(self):
        """
        Returns list of orders.
        """
        categories = OrderRepository.list_()
        return categories

    @rest_api.response(201, 'Order successfully created.')
    @rest_api.expect(order)
    @jwt_required
    def post(self):
        """
        Creates a new order.
        """
        data = request.json
        OrderRepository.create(data)
        return None, 201


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

    @rest_api.expect(order)
    @rest_api.response(204, 'Order successfully updated.')
    @jwt_required
    def patch(self, uuid):
        """
        Updates a order.
        Use this method to change the name of an Order.
        * Specify the UUID of the Order to modify in the request URL path.
        """
        data = request.json
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
