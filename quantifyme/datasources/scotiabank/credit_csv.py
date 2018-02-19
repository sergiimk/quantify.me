import re
import csv
import uuid
import arrow
from quantifyme.domain.model import Event


NAMESPACE_SCOTIA_CREDIT = uuid.UUID('5645fe08-85b0-426c-9982-155c00e19848')


def parse_csv(filename, tzinfo=None):
    with open(filename, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
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

    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_SCOTIA_CREDIT,
        name=':'.join((t.isoformat(), delta, desc))
    )

    return Event(
        id=id,
        t=t,
        delta=delta,
        desc=desc,
    )


if __name__ == '__main__':
    import sys
    import argparse
    from quantifyme.infra.codecs.json import JsonCodec

    parser = argparse.ArgumentParser(
        description='Parses Scotia Bank credit card history')
    parser.add_argument('file', nargs='*', help="the source CSV file")
    args = parser.parse_args()

    codec = JsonCodec()

    for filename in args.file:
        for event in parse_csv(filename):
            sys.stdout.write(codec.write(event).decode('utf8'))
            sys.stdout.write(',\n')
