from flask_restplus import fields

from app import rest_api

product = rest_api.model(
    'Product', {
        'uuid': fields.String(readOnly=True, description='The unique identifier of a product'),
        'name': fields.String(required=True, description='product name'),
        'price': fields.Arbitrary(required=True, description='product price'),
    })
