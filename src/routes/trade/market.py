from src.core.request import XRequest
from src.enums.trade import *


class Market:
    def __init__(self, headers):
        self.request = XRequest(headers)
        self.market_url = "/trade/v2/market"
        self.general_url = "/trade/v2"
        self.bulk_url = "/trade/v1/bulk"

    ###########
    # PAYLOAD #
    ###########

    def required_payload_post(  # noqa
            self,
            symbol: str,
            lot_size: float,
            order_type: OrderType = OrderType.sample_values(),
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            indicate: Indicate = Indicate.PRICE,
            **kwargs
    ):
        return dict(
            orderType=order_type,
            symbol=symbol,
            lotSize=lot_size,
            fillPolicy=fill_policy,
            indicate=indicate,
        ) | kwargs  # dictionary merging syntax

    def full_payload_post(
            self,
            symbol: str,
            lot_size: float,
            order_type: OrderType = OrderType.sample_values(),
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            indicate: Indicate = Indicate.PRICE,
            stop_loss: float = 0,
            take_profit: float = 0,
            **kwargs
    ):
        return dict(
            stopLoss=stop_loss, takeProfit=take_profit
        ) | self.required_payload_post(symbol, lot_size, order_type, fill_policy, indicate, **kwargs)

    def required_payload_patch(  # noqa
            self,
            order_id: str, symbol: str, **kwargs
    ):
        return dict(
            orderId=order_id, symbol=symbol
        ) | kwargs

    def full_payload_patch(
            self,
            order_id: str,
            symbol: str,
            stop_loss: float,
            take_profit: float,
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            indicate: Indicate = Indicate.PRICE,
            **kwargs
    ):
        return dict(
            fillPolicy=fill_policy,
            indicate=indicate,
            stopLoss=stop_loss,
            takeProfit=take_profit
        ) | self.required_payload_patch(order_id, symbol, **kwargs)

    def payload_put(  # noqa
            self,
            order_id: str,
            symbol: str,
            lot_size: float,
            order_type: OrderType = OrderType.sample_values(),
            fill_policy: FillPolicy = FillPolicy.FILL_OR_KILL,
            **kwargs
    ):
        return dict(
            orderId=order_id,
            orderType=order_type,
            symbol=symbol,
            lotSize=lot_size,
            fillPolicy=fill_policy,
            **kwargs
        )

    def payload_bulk(  # noqa
            self,
            order_id: str | list,
            symbol: str | list,
            lot_size: float | list,
            fill_policy: FillPolicy | list = FillPolicy.FILL_OR_KILL,
            **kwargs
    ):
        def __cast_to_list__(value):
            return value if isinstance(value, list) else [value]

        return dict(
            orderList=[
                dict(
                    orderId=__cast_to_list__(order_id)[i],
                    symbol=__cast_to_list__(symbol)[i],
                    lotSize=__cast_to_list__(lot_size)[i],
                    fillPolicy=__cast_to_list__(fill_policy)[i],
                    **kwargs
                ) for i in range(len(__cast_to_list__(order_id)))
            ]
        )

    ##########
    # METHOD #
    ##########

    def post_market(self, payload, **kwargs):
        resp = self.request.post(self.market_url, payload, **kwargs)
        return resp

    patch_market = post_market  # alias method

    def put_market(self, payload, **kwargs):
        resp = self.request.put(self.general_url, payload, **kwargs)
        return resp

    def put_bulk(self, payload, **kwargs):
        resp = self.request.put(self.bulk_url, payload, **kwargs)
        return resp

    ##########
    # SCHEMA #
    ##########
    @property
    def schema_post_market(self):
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

    schema_put_market = schema_post_market  # alias schema
    schema_patch_market = schema_post_market  # alias schema

    @property
    def schema_bulk(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "object",
                    "properties": {
                        "tenantId": {
                            "type": "string"
                        },
                        "account": {
                            "type": "string"
                        },
                        "horizonAccountType": {
                            "type": "string"
                        },
                        "traceId": {
                            "type": "string"
                        },
                        "closedOrderIds": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    },
                    "required": [
                        "tenantId",
                        "account",
                        "horizonAccountType",
                        "traceId",
                        "closedOrderIds"
                    ]
                }
            },
            "required": [
                "code",
                "result"
            ]
        }
