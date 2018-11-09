import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_Production(self):
        self.assertFalse(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
