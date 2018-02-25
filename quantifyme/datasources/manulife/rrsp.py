import uuid
import arrow
import decimal
import simplejson
import jsonschema
from quantifyme.domain.model import Event


NAMESPACE_MANULIFE_RRSP = uuid.UUID('520158c5-84f4-44b9-a95e-0ab9faacbf79')


SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['t', 'delta', 'type'],
    'properties': {
        't': {'type': 'string'},
        'delta': {'type': 'number'},
        'type': {'type': 'string'},
        'investments': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['code', 'name', 'percentage'],
                'properties': {
                    'code': {'type': 'string'},
                    'name': {'type': 'string'},
                    'percentage': {'type': 'number'},
                }
            }
        }
    }
}


def parse_json(filename):
    with open(filename, 'rb') as f:
        data = simplejson.load(f, encoding='utf8', parse_float=decimal.Decimal)
        for obj in data:
            try:
                yield parse_obj(obj)
            except Exception as e:
                raise Exception(
                    "Failed to parse object: {!r}".format(obj)
                ) from e


def parse_obj(obj):
    jsonschema.validate(obj, SCHEMA)

    t = arrow.get(obj.pop('t'))
    delta = obj['delta']

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_MANULIFE_RRSP,
        name=':'.join((str(t), str(delta)))
    )

    return Event(
        id=id,
        t=t,
        **obj)
