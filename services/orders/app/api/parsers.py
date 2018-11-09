import os

from flask_restplus import reqparse

authentication_parser = reqparse.RequestParser()
authentication_parser.add_argument(os.environ['JWT_HEADER_NAME'], location='headers')

search_parser = reqparse.RequestParser()
search_parser.add_argument('product_uuid', location='args', help='attached product')
