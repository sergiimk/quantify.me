import http.client
from test_base import TsdbApiTestCase
import iso8601


class TestTSDB(TsdbApiTestCase):

    def test_get_empty(self):
        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.status_code, http.client.OK)
        self.assertEqual(resp.json, [])

    def test_get_data_file(self):
        resp = self.client.get('/sensors/1/file')
        self.assertEqual(resp.status_code, http.client.OK)
        self.assertIn('Content-Disposition', resp.headers)

    def test_append_data(self):
        event1 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc1'}
        event2 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc2'}

        resp = self.client.post('/sensors/1', data=[event1, event2])
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.json, [event1, event2])

        event3 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc3'}
        event4 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc4'}

        resp = self.client.post('/sensors/1', data=[event3, event4])
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.json, [event1, event2, event3, event4])

    def test_overwrite_data(self):
        event1 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc1'}
        event2 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc2'}

        resp = self.client.put('/sensors/1', data=[event1, event2])
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.json, [event1, event2])

        event3 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc3'}
        event4 = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc4'}

        resp = self.client.put('/sensors/1', data=[event3, event4])
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.json, [event3, event4])

    def test_delete_data(self):
        event = {'t': iso8601.format(iso8601.utcnow()), 'location': 'loc1'}
        resp = self.client.put('/sensors/1', data=[event])
        self.assertEqual(resp.status_code, http.client.CREATED)

        resp = self.client.delete('/sensors/1')
        self.assertEqual(resp.status_code, http.client.OK)

        resp = self.client.get('/sensors/1')
        self.assertEqual(resp.json, [])