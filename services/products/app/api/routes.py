from app import rest_api
from app.api.endpoints import ProductCollection, ProductItem

products_namespace = rest_api.namespace('', description='Operations related to products')

products_namespace.route('/')(ProductCollection)
products_namespace.route('/<string:uuid>')(ProductItem)
