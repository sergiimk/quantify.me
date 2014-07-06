import calendar
from datetime import datetime
import dateutil.parser


def format(dt):
    """
    Get datetime representation in ISO 8601 format.

    For timezone-unaware dates returns:
    'YYYY-MM-DDThh:mm:ss[.MICROS]'

    For timezone-aware:
    'YYYY-MM-DDThh:mm:ss[.MICROS](+-)hh:mm'

    For UTC:
    'YYYY-MM-DDThh:mm:ss[.MICROS]Z'
    """
    if dt.tzinfo is not None and dt.tzinfo.tzname(dt) == 'UTC':
        return dt.replace(tzinfo=None).isoformat() + 'Z'
    return dt.isoformat()


def parse(s):
    """
    Parse ISO 8601 dates and times into datetime object.

    When in no_timezones mode (default) all returned dates will be in UTC
    timezone-unaware format (as Django likes them).

    Examples:
    '2013-02-14' => datetime(2013, 02, 14, tzinfo=None)
    '15:59:31.123' => datetime(<current date>, 15, 59, 31, 123000, tzinfo=None)
    '1988-07-24T15:59:31' => datetime(... , tzinfo=None)
    '1988-07-24T15:59:31Z' => datetime(... , tzinfo=tzutc())
    '1988-07-24T15:59:31+10:00' => datetime(... , tzinfo=tzoffset(None, 36000))
    """
    return dateutil.parser.parse(s)


def to_utc_timestamp(dt):
    return calendar.timegm(dt.utctimetuple())


def from_utc_timestamp(ts):
    return datetime.utcfromtimestamp(ts)
