import uuid
import arrow
import jsonschema
from quantifyme.domain.model import Event


investment_schema = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['t', 'delta', 'desc'],
    'properties': {
        't': {'type': 'string'},
        'delta': {'type': 'number'},
        'desc': {'type': 'string'},
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


def parse_obj(obj, id_namespace):
    jsonschema.validate(obj, investment_schema)

    t = arrow.get(obj.pop('t'))
    delta = obj['delta']

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=id_namespace,
        name=':'.join((str(t), str(delta)))
    )

    return Event(
        id=id,
        t=t,
        **obj)
