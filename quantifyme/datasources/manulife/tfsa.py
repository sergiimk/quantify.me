import uuid
import decimal
import simplejson
from . import common


NAMESPACE_MANULIFE_TFSA = uuid.UUID('49abf6f4-75b8-4cf7-ab49-1937545a8ec5')


def parse(stream):
    data = simplejson.load(
        stream,
        encoding='utf8',
        parse_float=decimal.Decimal)

    for obj in data:
        try:
            yield common.parse_obj(
                obj,
                id_namespace=NAMESPACE_MANULIFE_TFSA)
        except Exception as e:
            raise Exception(
                "Failed to parse object: {!r}".format(obj)
            ) from e
