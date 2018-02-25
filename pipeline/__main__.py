import os
import logging
from quantifyme.infra.streams.chunked_json import ChunkedJsonWriter
from . import constants
from . import scotia_import
from . import scotia_categorize
from . import elastic_export
from quantifyme.datasources import manulife
from quantifyme.datasources import scotiabank


DATASOURCES = [{
    'name': constants.SCOTIA_ACCOUNT_CHQ,
    'pattern': '~/Documents/documents/stats/account history/'
               'scotia-chequing-*.csv',
    'parser': {
        'fun': scotiabank.chequing.parse_csv,
        'args': {'tzinfo': '-08:00'},
        'extra': {'account': constants.SCOTIA_ACCOUNT_CHQ},
    },
    'out_file': 'data/scotia-chequing.cjson',
    'elastic_index': 'transaction',
}, {
    'name': constants.SCOTIA_ACCOUNT_CREDIT,
    'pattern': '~/Documents/documents/stats/account history/'
               'scotia-credit-*.csv',
    'parser': {
        'fun': scotiabank.credit.parse_csv,
        'args': {'tzinfo': '-08:00'},
        'extra': {'account': constants.SCOTIA_ACCOUNT_CREDIT},
    },
    'out_file': 'data/scotia-credit.cjson',
    'elastic_index': 'transaction',
}, {
    'name': constants.MANULIFE_ACCOUNT_RRSP,
    'pattern': '~/Documents/documents/stats/account history/'
               'manulife-rrsp-*.json',
    'parser': {
        'fun': manulife.rrsp.parse_json,
        'args': {},
        'extra': {'account': constants.MANULIFE_ACCOUNT_RRSP},
    },
    'out_file': 'data/manulife-rrsp.cjson',
    'elastic_index': 'transaction',
}]


def serialize_events(events, filename):
    outdir = os.path.dirname(filename)
    os.makedirs(outdir, exist_ok=True)

    events = list(events)
    events.sort(key=lambda e: (e.t, e.id))

    with open(filename, mode='wb') as f:
        writer = ChunkedJsonWriter(f, pretty=True)
        for e in events:
            writer.write(e)


def main():
    for src in DATASOURCES:
        elastic_export.recreate_index(src['elastic_index'])

    for src in DATASOURCES:
        logging.info(
            'Reading data for: %s', src['name'])
        events = scotia_import.read_events(src)

        logging.info(
            'Categorizing events')
        scotia_categorize.categorize(events)

        logging.info(
            'Dumping to file: %s', src['out_file'])
        serialize_events(events, src['out_file'])

        logging.info(
            'Exporting to ElasticSearch index: %s', src['elastic_index'])
        elastic_export.export(events, src['elastic_index'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
