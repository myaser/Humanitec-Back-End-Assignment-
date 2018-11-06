import os

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_simple import JWTManager

from app.api import rest_api
from app.api.routes import products_namespace


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register apis
    blueprint = Blueprint('api', __name__, url_prefix='/products')
    rest_api.init_app(blueprint)
    rest_api.add_namespace(products_namespace)
    app.register_blueprint(blueprint)

    JWTManager(app)

    return app
