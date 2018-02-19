import os
import glob


def read_events(src):
    pattern = os.path.expanduser(src['pattern'])
    filenames = glob.glob(pattern)
    events = {
        e
        for f in filenames
        for e in src['parser']['fun'](f, **src['parser']['args'])
    }

    for e in events:
        for k, v in src['parser']['extra'].items():
            setattr(e, k, v)

    return events

