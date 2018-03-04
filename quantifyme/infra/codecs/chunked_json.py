import io
import simplejson
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event


###############################################################################

class ChunkedJsonWriter:

    def __init__(self, stream, pretty=False):
        self._stream = stream
        self._pretty = pretty

    def write(self, event):
        js = simplejson.dumps(
            event,
            default=self._encode,
            use_decimal=True,
            sort_keys=True,
            indent=2 if self._pretty else None,
            allow_nan=False,
            check_circular=False,
            ensure_ascii=False,
        )

        chunk = js.encode('utf8')

        size = len(chunk)
        if self._pretty:
            size += 1

        prefix = str(size).encode('utf8')

        self._stream.write(prefix)
        self._stream.write(chunk)

        if self._pretty:
            self._stream.write(b'\n')

    def _encode(self, o):
            if isinstance(o, Event):
                return o.__dict__
            if isinstance(o, (uuid.UUID, arrow.Arrow)):
                return str(o)

            raise TypeError(
                "Object of type '{}' is not JSON serializable"
                .format(type(o).__name__))


###############################################################################

class ChunkedJsonReader:
    MAX_CHUNK_SIZE_LEN = len(str(2**64)) + 1

    def __init__(self, stream):
        self._stream = io.BufferedReader(
            raw=stream,
            buffer_size=self.MAX_CHUNK_SIZE_LEN)

    def read(self):
        prefix = self._stream.peek(self.MAX_CHUNK_SIZE_LEN)
        prefix = self._stream.read(prefix.find(b'{'))
        size = int(prefix)
        chunk = self._stream.read(size)

        raw = simplejson.loads(
            chunk.decode('utf8'),
            parse_float=decimal.Decimal,
        )

        raw['id'] = uuid.UUID(raw['id'])
        raw['t'] = arrow.get(raw['t'])
        return Event(**raw)
