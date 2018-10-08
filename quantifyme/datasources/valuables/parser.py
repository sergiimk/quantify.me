import arrow
import decimal
import jsonschema
import simplejson
import uuid
from quantifyme.domain.model import Event


NAMESPACE_VALUABLES = uuid.UUID('f311ef40-c413-4f0e-afb0-1d85da2d5ed1')


VALUABLES_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['t', 'desc', 'book_value', 'kind'],
    'properties': {
        't': {
            'type': 'string',
            'format': 'date-time',
        },
        'desc': {
            'type': 'string',
        },
        'book_value': {
            'type': 'number',
        },
        'kind': {
            'type': 'string',
        }
    }
}


def parse(stream):
    data = simplejson.load(
        stream,
        encoding='utf8',
        parse_float=decimal.Decimal)

    for obj in data:
        try:
            yield parse_object(obj)
        except Exception as e:
            raise Exception(
                "Failed to parse object: {!r}".format(obj)
            ) from e


def parse_object(obj):
    jsonschema.validate(obj, VALUABLES_SCHEMA)

    t = arrow.get(obj.pop('t'))

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_VALUABLES,
        name=':'.join(
            (str(t), obj['desc'], obj['kind'],
             str(obj['book_value']))
        )
    )

    return Event(
        id=id,
        t=t,
        **obj)
