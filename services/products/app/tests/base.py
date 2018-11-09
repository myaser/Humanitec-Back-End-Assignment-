from flask_jwt_simple import create_jwt
from flask_testing import TestCase

from app import create_app
from app.gateways import get_default_gateway


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        self.test_jwt_token = create_jwt('username')

    def tearDown(self):
        get_default_gateway().purge()
