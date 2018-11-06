from flask_testing import TestCase

from app import create_app


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
