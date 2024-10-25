import os
from enum import Enum

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_FILE_PATH = os.path.join(DATA_DIR, 'config.json')


class Uri(Enum):
    DASHBOARD = ''
    CART = '/cart/'
    CHECKOUT = '/checkout/'
    MY_ACCOUNT = '/my-account/'
    PRIVACY_POLICY = '/privacy-policy/'
    REFUND_RETURNS = '/refund_returns/'
    SHOP = '/shop/'


class Wait:
    SHORT_WAIT = 3
    MID_WAIT = 5
    LONG_WAIT = 10
