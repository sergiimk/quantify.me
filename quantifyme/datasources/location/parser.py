import arrow
import decimal
import jsonschema
import iso3166
import simplejson
import uuid
from quantifyme.domain.model import Event


NAMESPACE_LOCATION = uuid.UUID('e688b6e4-1493-4069-8440-849e4f4cdb79')


LOCATION_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['t', 'country', 'city', 'transport'],
    'properties': {
        'id': {
            'type': 'string',
            'format': 'uuid',
        },
        't': {
            'type': 'string',
            'format': 'date-time',
        },
        'country': {
            'type': 'string',
            'enum': list(iso3166.countries_by_alpha2.keys()),
        },
        'city': {
            'type': 'string',
        },
        'transport': {
            'type': 'string',
        },
        'geohash': {
            'type': 'string',
        }
    }
}


def parse(stream):
    locations = simplejson.load(
        stream,
        encoding='utf8',
        parse_float=decimal.Decimal)

    for loc in locations:
        try:
            yield parse_location(loc)
        except Exception as e:
            raise Exception(
                "Failed to parse object: {!r}".format(loc)
            ) from e


def parse_location(obj):
    jsonschema.validate(obj, LOCATION_SCHEMA)

    t = arrow.get(obj.pop('t'))

    id = obj.pop('id', None)
    if id:
        id = uuid.UUID(id)
    else:
        # Create stable ID based on input data
        id = uuid.uuid5(
            namespace=NAMESPACE_LOCATION,
            name=':'.join((str(t), obj['country'], obj['city'])))

    return Event(
        id=id,
        t=t,
        **obj)
