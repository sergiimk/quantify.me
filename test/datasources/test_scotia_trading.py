import io
import uuid
import arrow
import decimal
from quantifyme.domain import model
from quantifyme.datasources.scotiabank import trading


def test_parsing():
    data = '''Description,Symbol,Transaction Date,Settlement Date,Account Currency,Type,Quantity,Currency of Price,Price,Settlement Amount
INVESCO QQQ INDEX ETF CAD HEDGED UNIT    ,QQC.F,10-Aug-2018,14-Aug-2018,CAD,BUY,1.00,CAD,63.930,-1000.00,'''
    stream = io.BytesIO(data.encode('utf8'))
    result = list(trading.parse(stream))
    assert result == [
        model.Event(
            id=uuid.UUID('adca2a67-5e11-5750-a584-f7ff2c3f310e'),
            t=arrow.Arrow(2018, 8, 10),
            currency_of_price='CAD',
            delta=decimal.Decimal('-1000.00'),
            desc='INVESCO QQQ INDEX ETF CAD HEDGED UNIT',
            item_price=decimal.Decimal('63.930'),
            operation_type='buy',
            quantity=decimal.Decimal('1.00'),
            settlement_date='2018-08-14T00:00:00+00:00',
            symbol='QQC.F')
    ]
