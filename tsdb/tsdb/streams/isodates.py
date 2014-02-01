from dateutil.tz import tzutc, gettz
from dateutil.parser import parse
from datetime import datetime
import calendar

class isodates:
    @staticmethod
    def now():
        return datetime.now(gettz(None))

    @staticmethod
    def utcnow():
        return datetime.now(tzutc())

    @staticmethod
    def to_utc_timestamp(dt):
        return calendar.timegm(dt.utctimetuple())

    @staticmethod
    def from_utc_timestamp(ts):
        return datetime.utcfromtimestamp(ts).replace(tzinfo=tzutc())

    @staticmethod
    def format(dt):
        if isinstance(dt.tzinfo, tzutc):
            return dt.replace(tzinfo=None).isoformat() + 'Z'
        return dt.isoformat()

    @staticmethod
    def parse(s):
        return parse(s)
