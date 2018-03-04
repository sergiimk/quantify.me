import logging
from . import constants
from quantifyme.datasources import (
    location,
    manulife,
    scotiabank,
)
from .importers import reader
from .enrich import (
    geodata,
    scotia_categorize,
)
from .exporters import (
    chunked_json,
    elasticsearch,
    influxdb,
)


DATASOURCES = [{
    'name': constants.SCOTIA_ACCOUNT_CHQ,
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'scotia-chequing-*.csv',
    'parser': {
        'fun': scotiabank.chequing.parse,
        'args': {'tzinfo': '-08:00'},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.SCOTIA_ACCOUNT_CHQ,
        },
    },
    'out_file': 'data/scotia-chequing.cjson',
}, {
    'name': constants.SCOTIA_ACCOUNT_CREDIT,
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'scotia-credit-*.csv',
    'parser': {
        'fun': scotiabank.credit.parse,
        'args': {'tzinfo': '-08:00'},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.SCOTIA_ACCOUNT_CREDIT,
        },
    },
    'out_file': 'data/scotia-credit.cjson',
}, {
    'name': constants.MANULIFE_ACCOUNT_RRSP,
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'manulife-rrsp-*.json',
    'parser': {
        'fun': manulife.rrsp.parse,
        'args': {},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.MANULIFE_ACCOUNT_RRSP,
        },
    },
    'out_file': 'data/manulife-rrsp.cjson',
}, {
    'name': constants.MANULIFE_ACCOUNT_TFSA,
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'manulife-tfsa-*.json',
    'parser': {
        'fun': manulife.tfsa.parse,
        'args': {},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.MANULIFE_ACCOUNT_TFSA,
        },
    },
    'out_file': 'data/manulife-tfsa.cjson',
}, {
    'name': 'Location',
    'type': constants.TYPE_LOCATION,
    'pattern': '~/Documents/documents/stats/location.json',
    'parser': {
        'fun': location.parse,
        'args': {},
        'extra': {'type': constants.TYPE_LOCATION},
    },
    'out_file': 'data/location.cjson',
}]


def main():
    elastic_exporter = elasticsearch.ElasticSearchExporter()

    for type in {s['type'] for s in DATASOURCES}:
        elastic_exporter.recreate_index(type)

    for src in DATASOURCES:
        logging.info(
            'Reading data for: %s', src['name'])
        events = set(reader.read_events(src))

        if src['type'] == constants.TYPE_LOCATION:
            logging.info('Geo-tagging events')
            geodata.add_geodata(events)

        if src['type'] == constants.TYPE_TRANSACTION:
            logging.info(
                'Categorizing events')
            scotia_categorize.categorize(events)

        logging.info(
            'Dumping to file: %s', src['out_file'])
        chunked_json.export(events, src['out_file'])

        logging.info('Exporting to ElasticSearch: {}'.format(src['type']))
        elastic_exporter.export(events, src['type'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
