import unittest
import sqlite3
from test_client import TestClient
import tsdbapi


class TsdbApiTestCase(unittest.TestCase):

    def setUp(self):
        cs = 'file:db?mode=memory&cache=shared'
        self._db = sqlite3.connect(cs)
        tsdbapi.init_db(self._db)

        tsdbapi.app.config['DATABASE'] = cs
        tsdbapi.app.config['TESTING'] = True

        tsdbapi.app.test_client_class = TestClient
        self.client = tsdbapi.app.test_client()

    def tearDown(self):
        self._db.close()