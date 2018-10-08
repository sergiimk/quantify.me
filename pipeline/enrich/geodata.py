import geocoder
import geohash2


def add_geodata(events, cache=None, google_api_key=None):
    if cache is None:
        cache = {}

    for e in events:
        if hasattr(e, 'geohash'):
            continue

        geodata = cache.get((e.country, e.city))
        if not geodata:
            geodata = geocoder.google(
                '{}, {}'.format(e.city, e.country),
                key=google_api_key)
            if not geodata:
                raise Exception(
                    'Failed to lookup location data for: {}\n'
                    'Response: {}'.format(e, geodata))

            cache[(e.country, e.city)] = geodata

        e.geohash = geohash2.encode(*geodata.latlng)
