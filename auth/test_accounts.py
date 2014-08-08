import http.client
from test_base import AuthTestCase


class TestCreateAccount(AuthTestCase):

    def test_get_all_empty_db(self):
        resp = self.client.get('/accounts')
        self.assertEqual(resp.status_code, http.client.OK)
        self.assertEqual(resp.json, {
            'accounts': [],
        })

    def test_register_success(self):
        resp = self.client.post('/accounts', data={
            'email': 'test@example.com',
            'password': 'swordfish',
        })
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.get('/accounts')
        self.assertEqual(resp.status_code, http.client.OK)
        self.assertEqual(resp.json, {
            'accounts': [{
                'account_id': 1,
                'email': 'test@example.com',
            }],
        })
