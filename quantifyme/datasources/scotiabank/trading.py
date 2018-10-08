import io
import re
import csv
import uuid
import arrow
import decimal
from quantifyme.domain.model import Event


NAMESPACE_SCOTIA_TRADING = uuid.UUID('f776c9d8-ff46-4841-a3f3-0ebb00838486')


def parse(stream, tzinfo=None):
    stream = io.TextIOWrapper(stream, encoding='utf8')
    reader = csv.reader(stream)
    for row in reader:
        if row[0] == 'Description':
            continue
        try:
            yield parse_row(row, tzinfo=tzinfo)
        except Exception as e:
            raise Exception("Failed to parse row: {!r}".format(row)) from e


def parse_row(row, tzinfo=None):
    (
        desc,
        symbol,
        transaction_date,
        settlement_date,
        account_currency,
        operation_type,
        quantity,
        currency_of_price,
        item_price,
        settlement_amount,
        _
    ) = row

    desc = desc.strip()
    desc = re.sub(' +', ' ', desc)
    symbol = symbol.strip().upper()
    transaction_date = arrow.get(transaction_date, 'DD-MMM-YYYY', tzinfo=tzinfo)
    settlement_date = arrow.get(settlement_date, 'DD-MMM-YYYY', tzinfo=tzinfo)
    account_currency = account_currency.strip().upper()
    operation_type = operation_type.strip().lower()
    quantity = decimal.Decimal(quantity)
    currency_of_price = currency_of_price.strip().upper()
    item_price = decimal.Decimal(item_price)
    settlement_amount = decimal.Decimal(settlement_amount)

    t = transaction_date
    # Create stable ID based on input data
    id = uuid.uuid5(
        namespace=NAMESPACE_SCOTIA_TRADING,
        name=':'.join((str(t), str(settlement_amount), symbol))
    )

    return Event(
        id=id,
        t=t,
        desc=desc,
        symbol=symbol,
        operation_type=operation_type,
        item_price=item_price,
        currency_of_price=currency_of_price,
        quantity=quantity,
        settlement_date=str(settlement_date),
        delta=settlement_amount,
    )
