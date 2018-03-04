import os
import glob


def read_events(src):
    parse = src['parser']['fun']
    parse_args = src['parser']['args']
    event_extra = src['parser']['extra']

    pattern = os.path.expanduser(src['pattern'])
    filenames = glob.glob(pattern)

    for fname in filenames:
        with open(fname, 'rb') as f:
            for e in parse(f, **parse_args):
                for k, v in event_extra.items():
                    setattr(e, k, v)

                yield e
