import re
import logging
from .. import constants


logger = logging.getLogger(__name__)


def is_transfer(e):
    if not hasattr(e, 'desc'):
        return False

    return ((
        e.account == constants.SCOTIA_ACCOUNT_CHQ and
        e.desc == 'Customer Transfer Dr. PC TO 4537049644328016'
    ) or (
        e.account == constants.SCOTIA_ACCOUNT_CREDIT and
        e.desc == 'PC - PAYMENT FROM - *****10*4784'
    ))


def is_asset(e):
    if not hasattr(e, 'desc'):
        return False

    goods_stores = ('IKEA', 'WAL-MART', 'FUTURE SHOP')
    return any(store in e.desc for store in goods_stores)


tag_by_desc = (
    ('Initial balance', ('correction',)),
    ('Audible', ('education', 'books')),
    ('CENTRAL PLAZA', ('rent',)),
    ('COMPASS', ('transportation', 'transit')),
    ('Payroll Deposit DEMONWARE', ('salary',)),
    ('HOLLYBURN', ('rent',)),
    ('WAL-MART', ('goods',)),
    ('HOME DEPOT', ('goods',)),
    ('FUTURE SHOP', ('goods',)),
    ('IKEA', ('goods', 'furniture',)),
    ('7-ELEVEN', ('food',)),
    ('IGA #', ('food',)),
    ('SAFEWAY', ('food',)),
    ('LIQUOR', ('food', 'liquor')),
    ('HYDRO', ('utilities', 'electricity')),
    ('SHAW', ('utilities', 'internet')),
    ('SHELL', ('transportation', 'fuel')),
    ('PETROCAN', ('transportation', 'fuel')),
    ('CHEVRON', ('transportation', 'fuel')),
    ('CHATR', ('utilities', 'phone')),
    ('BELL MOBILITY', ('utilities', 'phone')),
    ('NETFLIX', ('entertainment', 'video')),
    ('HULU\\.COM', ('entertainment', 'video')),
    ('PLAYSTATION', ('entertainment', 'games')),
    ('TRANSLINK', ('transportation', 'transit')),
    ('CAR2GO', ('transportation', 'car')),
    ('ALASKA AIR', ('transportation', 'air')),
    ('HARBOUR CENTRE DENTAL', ('medical',)),
    ('SQUARE ONE INSURANCE', ('utilities', 'insurance')),
    ('TIM HORTONS', ('food', 'restaurants')),
)


def get_tags(e):
    if not hasattr(e, 'desc'):
        return None

    tags = set()

    for p, tag in tag_by_desc:
        if re.search(p, e.desc, re.I):
            tags.update(tag)

    return list(tags)


def categorize(events):
    for e in events:
        tags = get_tags(e)
        if tags:
            e.tags = tags
            logger.debug('Tagging %s with tags: %s', e, tags)
        if is_transfer(e):
            e.transfer = True
            logger.debug('Marking %s as transfer', e)
        if is_asset(e):
            e.asset = True
            logger.debug('Marking %s as asset', e)
        if not tags and not is_transfer(e) and not is_asset(e):
            logger.warning('Uncategorized event %s', e)
