import unittest
import sqlite3
from test_client import TestClient
import accounts


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        cs = 'file:db?mode=memory&cache=shared'
        self._db = sqlite3.connect(cs)
        accounts.init_db(self._db)

        accounts.app.config['DATABASE'] = cs
        accounts.app.config['TESTING'] = True

        accounts.app.test_client_class = TestClient
        self.client = accounts.app.test_client()

    def tearDown(self):
        self._db.close()