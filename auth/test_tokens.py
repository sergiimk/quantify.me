import http.client
from unittest.mock import ANY
from test_base import AuthTestCase


class TestTokensPassword(AuthTestCase):

    def test_success(self):
        resp = self.client.post('/accounts', data={
            'email': 'test@example.com',
            'password': 'swordfish',
        })
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.post('/tokens', data={
            'grant_type': 'password',
            'email': 'test@example.com',
            'password': 'swordfish',
        })
        self.assertEqual(resp.status_code, http.client.OK)
        self.assertEqual(resp.json, {
            'account_id': 1,
            'access_token': ANY,
            'expires_in': 3600,
        })

    def test_account_does_not_exist(self):
        resp = self.client.post('/tokens', data={
            'grant_type': 'password',
            'email': 'test@example.com',
            'password': 'swordfish',
        })
        self.assertEqual(resp.status_code, http.client.UNAUTHORIZED)

    def test_invalid_password(self):
        resp = self.client.post('/accounts', data={
            'email': 'test@example.com',
            'password': 'swordfish',
        })
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.post('/tokens', data={
            'grant_type': 'password',
            'email': 'test@example.com',
            'password': 'clownfish',
        })
        self.assertEqual(resp.status_code, http.client.UNAUTHORIZED)
