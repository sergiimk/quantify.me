import os
from quantifyme.infra.codecs.chunked_json import ChunkedJsonWriter


def export(events, filename):
    outdir = os.path.dirname(filename)
    os.makedirs(outdir, exist_ok=True)

    events = list(events)
    events.sort(key=lambda e: (e.t, e.id))

    with open(filename, mode='wb') as f:
        writer = ChunkedJsonWriter(f, pretty=True)
        for e in events:
            writer.write(e)
