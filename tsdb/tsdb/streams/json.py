import json
from .isodates import isodates


# TODO: use sax to handle big data
class JsonStream:

    _read = None
    _read_idx = 0
    _written = 0

    def __init__(self, fs):
        self._fs = fs

    def read(self):
        if self._read is None:
            self._read = json.load(self._fs)

        if self._read_idx == len(self._read):
            return None

        event = self._read[self._read_idx]
        self._read_idx += 1

        event['t'] = isodates.parse(event['t'])
        return event

    # TODO: destructive optimization
    def write(self, event):
        event = dict(event)
        event['t'] = isodates.format(event['t'])

        l = json.dumps(event)

        if self._written:
            self._fs.write(',\n')
        self._written += 1
        self._fs.write(l)
        self._fs.write('')

    def write_start(self):
        self._fs.write('[\n')

    def write_end(self):
        self._fs.write('\n]')

    def __iter__(self):
        return self

    def __next__(self):
        event = self.read()
        if event is None:
            raise StopIteration
        return event
