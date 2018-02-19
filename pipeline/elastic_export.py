import glob
import elasticsearch.helpers


def _event_to_document(e):
    raw = dict(e.__dict__)
    raw['id'] = str(raw['id'])
    raw['t'] = str(raw['t'])
    raw['delta'] = float(raw['delta'])
    return raw


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
