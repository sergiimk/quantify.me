import re
import csv
import datetime


def parse_csv(filename):
    with open(filename, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                yield parse_row(row)
            except Exception as e:
                raise Exception("Failed to parse row: {!r}".format(row)) from e


def parse_row(row):
    date, delta, _, typ, desc = row
    mm, dd, yy = map(int, date.split('/'))
    t = datetime.datetime(2000 + yy, mm, dd)

    typ = typ.strip('" ')
    desc = desc.strip('" ')
    desc = re.sub(' +', ' ', desc)

    return {
        't': t,
        'delta': delta,
        'desc': ' '.join((typ, desc)),
    }


if __name__ == '__main__':
    import sys
    import argparse
    from . import utils

    parser = argparse.ArgumentParser(description='Parses Scotia Bank debit card history')
    parser.add_argument('file', nargs='*', help="the source CSV file")
    args = parser.parse_args()

    for filename in args.file:
        for event in parse_csv(filename):
            sys.stdout.write(utils.event_to_json_fragment(event))
            sys.stdout.write(',\n')
