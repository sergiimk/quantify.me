import click
import logging
from . import constants
from .datasources import DATASOURCES
from quantifyme.infra.codecs.chunked_json import ChunkedJsonReader
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


@click.group()
def cli():
    pass


@cli.command()
def ingest():
    """Import and enrich data"""
    all_in_one = []

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

        all_in_one.append({
            'name': src['name'],
            'events': [
                e.to_raw()
                for e in sorted(events, key=lambda e: (e.t, e.id))
            ]
        })

    with open('data/all_in_one.json', 'w', encoding='utf8') as f:
        import simplejson
        simplejson.dump(
            all_in_one, f,
            use_decimal=True,
            sort_keys=True,
            indent=2,
            allow_nan=False,
            check_circular=False,
            ensure_ascii=False)


@cli.command()
def export():
    """Export data to external tools"""
    for src in DATASOURCES:
        logging.info('Reading source: %s', src['name'])

        with open(src['out_file'], 'rb') as f:
            for e in ChunkedJsonReader(f):
                print(e)

    #from .exporters import (
    #elasticsearch,
    #influxdb,
    #)
    #elastic_exporter = elasticsearch.ElasticSearchExporter()
    #for type in {s['type'] for s in DATASOURCES}:
    #    elastic_exporter.recreate_index(type)
    # ...
    #logging.info('Exporting to ElasticSearch: {}'.format(src['type']))
    #elastic_exporter.export(events, src['type'])
    raise NotImplementedError()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
