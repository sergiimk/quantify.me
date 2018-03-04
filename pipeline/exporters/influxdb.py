import logging
from influxdb import InfluxDBClient


logger = logging.getLogger(__package__)


class InfluxDBExporter:
    def __init__(self, host='localhost', port=8086, username='admin',
                 password='admin', *, database):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database

    def _get_client(self, database=None):
        return InfluxDBClient(
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password,
            database=database)

    def recreate_database(self):
        client = self._get_client()
        client.drop_database(self._database)
        client.create_database(self._database)

    def export(self, events):
        client = self._get_client(database=self._database)
        points = (self._event_to_point(e) for e in events)
        client.write_points(list(points))

    # TODO
    def _event_to_point(self, e):
        try:
            raw = dict(e.__dict__)
            raw.pop('tags', None)
            raw.pop('investments', None)
            point = {
                'measurement': 'transaction',
                'time': str(raw.pop('t')),
                'tags': {
                    'account': raw.pop('account')
                },
                'fields': {
                    'value': float(raw.pop('delta')),
                    'id': str(raw.pop('id')),
                }
            }
            point['fields'].update(raw)
            return point
        except:
            logger.exception(
                'Failed to convert event to point: {}'.format(e))
            raise
