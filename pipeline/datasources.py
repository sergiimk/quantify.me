from . import constants
from quantifyme.datasources import (
    location,
    manulife,
    scotiabank,
    valuables,
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
    'name': constants.SCOTIA_ACCOUNT_TRADING,
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'scotia-trading-*.csv',
    'parser': {
        'fun': scotiabank.trading.parse,
        'args': {'tzinfo': '-08:00'},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.SCOTIA_ACCOUNT_TRADING,
        },
    },
    'out_file': 'data/scotia-trading.cjson',
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
    'name': 'Valuables',
    'type': constants.TYPE_TRANSACTION,
    'pattern': '~/Documents/documents/stats/account history/'
               'valuables.json',
    'parser': {
        'fun': valuables.parse,
        'args': {},
        'extra': {
            'type': constants.TYPE_TRANSACTION,
            'account': constants.VALUABLES,
        },
    },
    'out_file': 'data/valuables.cjson',
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
