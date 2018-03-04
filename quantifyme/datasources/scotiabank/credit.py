import io
import re
import csv
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event


NAMESPACE_SCOTIA_CREDIT = uuid.UUID('5645fe08-85b0-426c-9982-155c00e19848')


def parse(stream, tzinfo=None):
    stream = io.TextIOWrapper(stream, encoding='utf8')
    reader = csv.reader(stream)
    for row in reader:
        try:
            yield parse_row(row, tzinfo=tzinfo)
        except Exception as e:
            raise Exception("Failed to parse row: {!r}".format(row)) from e


def parse_row(row, tzinfo=None):
    date, desc, delta = row

    t = arrow.get(date, 'M/D/YY', tzinfo=tzinfo)
    desc = desc.strip('" ')
    desc = re.sub(' +', ' ', desc)

    delta = decimal.Decimal(delta)

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_SCOTIA_CREDIT,
        name=':'.join((str(t), str(delta), desc))
    )

    return Event(
        id=id,
        t=t,
        delta=delta,
        desc=desc,
    )
