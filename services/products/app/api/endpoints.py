from flask import request
from flask_jwt_simple import jwt_required
from flask_restplus import Resource, marshal

from app import rest_api
from app.api.parsers import authentication_parser
from app.api.serializers import product, product_update
from app.repositories import ProductRepository


@rest_api.expect(authentication_parser)
class ProductCollection(Resource):

    @rest_api.marshal_list_with(product)
    @jwt_required
    def get(self):
        """
        Returns list of products.
        """
        products = ProductRepository.list_()
        return products

    @rest_api.response(201, 'Product successfully created.')
    @rest_api.response(409, 'data integrity error.')
    @rest_api.expect(product, validate=True)
    @jwt_required
    def post(self):
        """
        Creates a new product.
        """
        # data = request.json
        data = marshal(request.json, product, skip_none=True)
        return ProductRepository.create(data), 201


@rest_api.response(404, 'Product not found.')
@rest_api.expect(authentication_parser)
class ProductItem(Resource):

    @rest_api.marshal_with(product)
    @jwt_required
    def get(self, uuid):
        """
        Returns a product
        """
        return ProductRepository.retrieve(uuid)

    @rest_api.expect(product_update, validate=True)
    @rest_api.response(204, 'Product successfully updated.')
    @jwt_required
    def patch(self, uuid):
        """
        Updates a product.
        Use this method to change the name of an Product.
        * Specify the UUID of the Product to modify in the request URL path.
        """
        data = marshal(request.json, product_update, skip_none=True)
        if data:
            ProductRepository.update(uuid, data)
        return None, 204

    @rest_api.response(204, 'Product successfully deleted.')
    @jwt_required
    def delete(self, uuid):
        """
        Deletes Product.
        """
        ProductRepository.delete(uuid)
        return None, 204
