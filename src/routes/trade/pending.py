import time

from src.core.request import XRequest
from src.enums.trade import *


class Pending:
    def __init__(self, headers):
        self.request = XRequest(headers)
        self.limit_url = "/trade/v2/limit"

    ###########
    # PAYLOAD #
    ###########

    def required_payload_post(  # noqa
            self,
            symbol: str,
            lot_size: float,
            price: float,
            order_type: OrderType = OrderType.sample_values(),
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            indicate: Indicate = Indicate.PRICE,
            trade_expiry: Expiry = Expiry.sample_values(),
            **kwargs
    ):
        return dict(
            orderType=order_type,
            symbol=symbol,
            lotSize=lot_size,
            fillPolicy=fill_policy,
            indicate=indicate,
            tradeExpiry=trade_expiry,
            price=price
        ) | kwargs  # dictionary merging syntax

    def full_payload_post(
            self,
            symbol: str,
            lot_size: float,
            price: float,
            order_type: OrderType = OrderType.sample_values(),
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            indicate: Indicate = Indicate.PRICE,
            trade_expiry: Expiry = Expiry.sample_values(),
            stop_loss: float = 0,
            take_profit: float = 0,
            expiration: float = round(time.time() + 5, 3),
            price_trigger: float = 0,
            **kwargs
    ):
        return dict(
            stopLoss=stop_loss, takeProfit=take_profit, expiration=expiration, priceTrigger=price_trigger,
        ) | self.required_payload_post(symbol, lot_size, price, order_type, fill_policy, indicate, trade_expiry, **kwargs)

    ##########
    # METHOD #
    ##########

    def post_limit(self, payload, **kwargs):
        resp = self.request.post(self.limit_url, payload, **kwargs)
        return resp

    ##########
    # SCHEMA #
    ##########

    @property
    def schema_post_limit(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "object",
                    "properties": {
                        "positionId": {
                            "type": "string"
                        },
                        "positionReference": {
                            "type": "string"
                        },
                        "clOrdId": {
                            "type": "string"
                        },
                        "traceId": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "positionId",
                        "positionReference",
                        "clOrdId",
                        "traceId"
                    ]
                }
            },
            "required": [
                "code",
                "result"
            ]
        }
