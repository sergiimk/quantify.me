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
        self._stream = stream
        self._buf = b''

    def _read(self, size):
        if not self._buf:
            return self._stream.read(size)

        if size <= len(self._buf):
            ret = self._buf[:size]
            self._buf = self._buf[size:]
            return ret

        ret = self._buf + self._stream.read(size - len(self._buf))
        self._buf = b''
        return ret

    def _unread(self, data):
        if not self._buf:
            self._buf = data
        else:
            self._buf += data

    def _read_chunk(self):
        size_prefix = self._read(self.MAX_CHUNK_SIZE_LEN)
        size_prefix_len = size_prefix.find(b'{')
        if size_prefix_len < 0:
            if not size_prefix:
                return b''
            raise ValueError('Malformed data')

        self._unread(size_prefix[size_prefix_len:])
        size_prefix = size_prefix[:size_prefix_len]

        size = int(size_prefix)
        return self._read(size)

    def read(self):
        chunk = self._read_chunk()
        if not chunk:
            return None

        raw = simplejson.loads(
            chunk.decode('utf8'),
            parse_float=decimal.Decimal,
        )

        raw['id'] = uuid.UUID(raw['id'])
        raw['t'] = arrow.get(raw['t'])
        return Event(**raw)

    def __iter__(self):
        while True:
            e = self.read()
            if not e:
                break
            yield e
