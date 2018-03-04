import sys
import logging
from .enrich import geodata
from quantifyme.datasources import location
from quantifyme.infra.codecs.json import JsonWriter


def main():
    events = list(location.parse(sys.stdin))
    cache = {}

    for e in events:
        try:
            geodata.add_geodata([e], cache=cache)
        except Exception:
            logging.exception('Error encountered - assuming rate limiting')
            break

    JsonWriter(sys.stdout).write(events)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
