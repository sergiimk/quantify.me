import json
import datetime


def json_serialize(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat() + 'Z'

    raise TypeError("Object of type '{!r}' is not JSON serializable".format(type(obj)))


def event_to_json_fragment(event):
    return json.dumps(
        event,
        sort_keys=True,
        indent=2,
        default=json_serialize)
