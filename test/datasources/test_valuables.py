import io
import uuid
import arrow
import decimal
from quantifyme.domain import model
from quantifyme.datasources.valuables import parser


def test_parsing():
    data = '''
[
  {
    "t": "2000-01-10T00:00:00+00:00",
    "desc": "Some Car",
    "book_value": 12345.00,
    "kind": "car"
  }
]
'''
    stream = io.BytesIO(data.encode('utf8'))
    result = list(parser.parse(stream))
    assert result == [
        model.Event(
            id=uuid.UUID('c74ce674-f852-5733-8198-45893435cb0e'),
            t=arrow.Arrow(2000, 1, 10),
            desc='Some Car',
            book_value=decimal.Decimal('12345.00'),
            kind='car',
        )
    ]
