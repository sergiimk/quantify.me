from flask.testing import FlaskClient
from flask import json
import unittest
import sqlite3
import accounts


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        content_type = kwargs.pop('content_type', None)

        if isinstance(data, dict):
            data = json.dumps(data)
            if not content_type:
                content_type = 'application/json'

        resp = super().open(
            *args,
            content_type=content_type,
            data=data,
            **kwargs)

        if resp.content_type == 'application/json':
            resp.json = json.loads(resp.data)

        return resp


class AccountsTestCase(unittest.TestCase):

    def setUp(self):
        cs = 'file:memdb1?mode=memory&cache=shared'
        self._db = sqlite3.connect(cs)
        accounts.init_db(self._db)

        accounts.app.config['DATABASE'] = cs
        accounts.app.config['TESTING'] = True

        accounts.app.test_client_class = TestClient
        self.client = accounts.app.test_client()

    def tearDown(self):
        self._db.close()