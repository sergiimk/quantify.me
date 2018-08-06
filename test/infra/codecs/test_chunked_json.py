import io
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event
from quantifyme.infra.codecs.chunked_json import (
    ChunkedJsonWriter,
    ChunkedJsonReader,
)


def test_write_events():
    stream = io.BytesIO()
    w = ChunkedJsonWriter(stream, pretty=False)
    w.write(Event(
        id=uuid.UUID('ed133d07-270d-4123-9d56-6a1f23919913'),
        t=arrow.get('2018-02-18T22:30:00-08:00'),
        data='test1',
    ))

    w.write(Event(
        id=uuid.UUID('7d1b7314-cc8d-4691-9fc4-c7cf645c70d1'),
        t=arrow.get('2018-02-18T22:40:00-08:00'),
        data='test2',
    ))

    assert stream.getvalue() == (
        b'97{"data": "test1", "id": "ed133d07-270d-4123-9d56-6a1f23919913", '
        b'"t": "2018-02-18T22:30:00-08:00"}'
        b'97{"data": "test2", "id": "7d1b7314-cc8d-4691-9fc4-c7cf645c70d1", '
        b'"t": "2018-02-18T22:40:00-08:00"}'
    )


def test_read_events():
    stream = io.BytesIO(
        b'97{"data": "test1", "id": "ed133d07-270d-4123-9d56-6a1f23919913", '
        b'"t": "2018-02-18T22:30:00-08:00"}'
        b'97{"data": "test2", "id": "7d1b7314-cc8d-4691-9fc4-c7cf645c70d1", '
        b'"t": "2018-02-18T22:40:00-08:00"}'
    )
    r = ChunkedJsonReader(stream)

    assert r.read() == Event(
        id=uuid.UUID('ed133d07-270d-4123-9d56-6a1f23919913'),
        t=arrow.get('2018-02-18T22:30:00-08:00'),
        data='test1',
    )

    assert r.read() == Event(
        id=uuid.UUID('7d1b7314-cc8d-4691-9fc4-c7cf645c70d1'),
        t=arrow.get('2018-02-18T22:40:00-08:00'),
        data='test2',
    )

    assert stream.read() == b''
