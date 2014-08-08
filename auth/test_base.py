import unittest
from test_client import TestClient
from accounts import app
from models import db


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_ECHO'] = True

        db.init_app(app)
        db.app = app
        db.create_all()

        app.test_client_class = TestClient
        self.client = app.test_client()
