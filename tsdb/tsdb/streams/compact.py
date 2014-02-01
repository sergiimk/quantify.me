import json
from .isodates import isodates


# TODO: optimize
class CompactStream:
    def __init__(self, fs):
        self._fs = fs

    def read(self):
        l = self._fs.readline()
        if not l:
            return None

        event = json.loads(l)

        ts = event['ts']
        event['t'] = self._stamp_to_date(ts)
        del event['ts']

        return event

    # TODO: destructive optimization
    def write(self, event):
        event = dict(event)

        ts = self._date_to_stamp(event['t'])
        event['ts'] = ts
        del event['t']

        l = json.dumps(event)
        self._fs.write(l)
        self._fs.write('\n')

    def __iter__(self):
        return self

    def __next__(self):
        e = self.read()
        if not e:
            raise StopIteration
        return e

    def _date_to_stamp(self, date):
        unix = isodates.to_utc_timestamp(date)
        return unix * 1000 + (date.microsecond // 1000)

    def _stamp_to_date(self, stamp):
        date = isodates.from_utc_timestamp(stamp // 1000)
        return date.replace(microsecond=stamp % 1000 * 1000)
