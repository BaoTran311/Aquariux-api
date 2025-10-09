from src.enums import BaseEnum


class OrderType(BaseEnum):
    BUY = 0
    SELL = 1


class FillPolicy(BaseEnum):
    FILL_OR_KILL = 0
    IMMEDIATE_OR_CANCEL = 1
    RETURN = 2


class Expiry(BaseEnum):
    GOOD_TILL_CANCELLED = "GTC"
    GOOD_TILL_DAY = "GTD"
    SPECIFIED_DATE = "SPECIFIED_DAY"
    SPECIFIED_DATE_AND_TIME = "SPECIFIED_TIMESTAMP"
