from flask_restplus import fields

from app import rest_api

product = rest_api.model(
    'Product', {
        'uuid': fields.String(readOnly=True, description='The unique identifier of a product', allow_null=False),
        'name': fields.String(required=True, description='product name', allow_null=False),
        'price': fields.Arbitrary(required=True, description='product price', allow_null=False),
    })

product_update = rest_api.model(
    'ProductUpdate', {
        'name': fields.String(required=False, description='product name', allow_null=False),
        'price': fields.Arbitrary(required=False, description='product price', allow_null=False),
    })
