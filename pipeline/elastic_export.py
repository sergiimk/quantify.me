import glob
import logging
import elasticsearch.helpers


logger = logging.getLogger(__package__)


def _event_to_document(e):
    try:
        raw = dict(e.__dict__)
        raw['id'] = str(raw['id'])
        raw['t'] = str(raw['t'])
        raw['delta'] = float(raw['delta'])
        return raw
    except:
        logger.exception('Failed to convert event to document: {}'.format(e))


def _index_bulk_action(index, doc):
    return {
        '_op_type': 'index',
        '_index': index,
        '_type': index,
        '_id': doc['id'],
        '_source': doc,
    }


def recreate_index(index):
    es = elasticsearch.Elasticsearch()

    try:
        es.indices.delete(index)
    except elasticsearch.exceptions.NotFoundError:
        pass

    es.indices.create(index)


def export(events, index):
    es = elasticsearch.Elasticsearch()

    documents = (
        _event_to_document(e)
        for e in events
    )

    actions = (
        _index_bulk_action(index, doc)
        for doc in documents
    )

    elasticsearch.helpers.bulk(
        client=es,
        actions=actions)
