import re
import csv
import uuid
import arrow
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
    typ = typ.strip('" ')
    desc = desc.strip('" ')
    desc = re.sub(' +', ' ', desc)

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_SCOTIA_CHQ,
        name=':'.join((t.isoformat(), delta, typ, desc))
    )

    return Event(
        id=id,
        t=t,
        delta=delta,
        desc=' '.join((typ, desc)),
    )


if __name__ == '__main__':
    import sys
    import argparse
    from quantifyme.infra.codecs.json import JsonCodec

    parser = argparse.ArgumentParser(
        description='Parses Scotia Bank chequing account history')
    parser.add_argument('file', nargs='*', help="the source CSV file")
    args = parser.parse_args()

    codec = JsonCodec()

    for filename in args.file:
        for event in parse_csv(filename):
            sys.stdout.write(codec.write(event).decode('utf8'))
            sys.stdout.write(',\n')
