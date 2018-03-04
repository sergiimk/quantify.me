import simplejson
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event


###############################################################################

class JsonWriter:

    def __init__(self, stream):
        self._stream = stream

    def write(self, events):
        events = list(events)
        events.sort(key=lambda e: (e.t, e.id))

        simplejson.dump(
            events,
            self._stream,
            default=self._encode,
            use_decimal=True,
            sort_keys=True,
            indent=2,
            allow_nan=False,
            check_circular=False,
            ensure_ascii=False,
            encoding='utf8')

    def _encode(self, o):
            if isinstance(o, Event):
                return o.__dict__
            if isinstance(o, (uuid.UUID, arrow.Arrow)):
                return str(o)

            raise TypeError(
                "Object of type '{}' is not JSON serializable"
                .format(type(o).__name__))


###############################################################################

class JsonReader:
    def __init__(self, stream):
        self._stream = stream

    def read(self):
        raw_events = simplejson.load(
            self._stream,
            encoding='utf8',
            parse_float=decimal.Decimal,
        )

        return [self._decode(raw) for raw in raw_events]

    def _decode(self, raw):
        raw['id'] = uuid.UUID(raw['id'])
        raw['t'] = arrow.get(raw['t'])
        return Event(**raw)
