import uuid
import decimal
import simplejson
from . import common


NAMESPACE_MANULIFE_RRSP = uuid.UUID('520158c5-84f4-44b9-a95e-0ab9faacbf79')


def parse(stream):
    data = simplejson.load(
        stream,
        encoding='utf8',
        parse_float=decimal.Decimal)

    for obj in data:
        try:
            yield common.parse_obj(
                obj,
                id_namespace=NAMESPACE_MANULIFE_RRSP)
        except Exception as e:
            raise Exception(
                "Failed to parse object: {!r}".format(obj)
            ) from e