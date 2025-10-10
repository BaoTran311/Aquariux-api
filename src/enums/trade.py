from src.enums import BaseEnum


class OrderType(BaseEnum):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BUY_STOP_LIMIT = 8
    SELL_STOP_LIMIT = 9


class FillPolicy(BaseEnum):
    FILL_OR_KILL = 0
    IMMEDIATE_OR_CANCEL = 1
    RETURN = 3


class Expiry(BaseEnum):
    GOOD_TILL_CANCELLED = "GTC"
    GOOD_TILL_DAY = "GTD"
    SPECIFIED_DATE = "SPECIFIED_DAY"
    SPECIFIED_DATE_AND_TIME = "SPECIFIED_TIMESTAMP"


class Indicate(BaseEnum):
    PRICE = "PRICE"
    POINTS = "POINTS"