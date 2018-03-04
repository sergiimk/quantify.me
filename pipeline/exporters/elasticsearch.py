import arrow
import decimal
import uuid
import logging
import elasticsearch.helpers


logger = logging.getLogger(__package__)


class ElasticSearchExporter:
    INDEX_BODY = {
        'mappings': {
            '_doc': {
                'properties': {
                    't': {'type': 'date'},
                    'delta': {'type': 'double'},
                    'geohash': {'type': 'geo_point'},
                }
            }
        }
    }

    def __init__(self):
        pass

    def _get_client(self):
        return elasticsearch.Elasticsearch()

    def recreate_index(self, index):
        client = self._get_client()

        try:
            client.indices.delete(index)
        except elasticsearch.exceptions.NotFoundError:
            pass

        client.indices.create(index, body=self.INDEX_BODY)

    def export(self, events, index):
        client = self._get_client()

        documents = (
            self._event_to_document(e)
            for e in events
        )

        actions = (
            self._index_bulk_action(index, doc)
            for doc in documents
        )

        elasticsearch.helpers.bulk(
            client=client,
            actions=actions)

    def _event_to_document(self, e):
        try:
            return self._to_raw(e.__dict__)
        except Exception:
            logger.exception('Failed to convert event to document: {}'.format(e))
            raise

    def _to_raw(self, obj):
        if isinstance(obj, dict):
            return {
                k: self._to_raw(v)
                for k, v in obj.items()
            }
        if isinstance(obj, list):
            return [self._to_raw(v) for v in obj]
        if isinstance(obj, (int, float, str)):
            return obj
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, arrow.Arrow):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise NotImplementedError(
            "Don't know how to represent value: {!r}".format(obj))

    def _index_bulk_action(self, index, doc):
        return {
            '_op_type': 'index',
            '_index': index,
            '_type': '_doc',
            '_id': doc['id'],
            '_source': doc,
        }
