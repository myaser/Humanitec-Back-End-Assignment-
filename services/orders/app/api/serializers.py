from flask_restplus import fields

from app import rest_api

order = rest_api.model(
    'Order', {
        'uuid': fields.String(readOnly=True, description='The unique identifier of a order'),
        'quantity': fields.Integer(required=True, description='quantity of product'),
        'product_uuid': fields.String(required=True, description='the unique identifier of product'),
    })

quantity = rest_api.model(
    'Quantity', {
        'quantity': fields.Integer(required=True, description='quantity of product'),
    })
