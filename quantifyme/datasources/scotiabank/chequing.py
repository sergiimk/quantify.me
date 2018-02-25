import re
import csv
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event


NAMESPACE_SCOTIA_CHQ = uuid.UUID('8c2637c7-468a-4e68-a8a2-27025f8a2ed5')


def parse_csv(filename, tzinfo=None):
    with open(filename, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                yield parse_row(row, tzinfo=tzinfo)
            except Exception as e:
                raise Exception("Failed to parse row: {!r}".format(row)) from e


def parse_row(row, tzinfo=None):
    date, delta, _, typ, desc = row

    t = arrow.get(date, 'M/D/YY', tzinfo=tzinfo)

    delta = decimal.Decimal(delta)

    typ = typ.strip('" ')
    desc = desc.strip('" ')
    desc = re.sub(' +', ' ', desc)

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_SCOTIA_CHQ,
        name=':'.join((str(t), str(delta), typ, desc))
    )

    return Event(
        id=id,
        t=t,
        delta=delta,
        desc=' '.join((typ, desc)),
    )
