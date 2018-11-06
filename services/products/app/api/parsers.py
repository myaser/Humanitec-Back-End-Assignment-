import os

from flask_restplus import reqparse

authentication_parser = reqparse.RequestParser()
authentication_parser.add_argument(os.environ['JWT_HEADER_NAME'], location='headers')
