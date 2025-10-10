from src.core.request import XRequest


class Order:
    def __init__(self, headers):
        self.request = XRequest(headers)
        self.counts_url = "/trade/order/v1/counts"
        self.general_url = "/trade/order/v1"
        self.order_pending_url = "/trade/order/v1/pending"

    ###########
    # PAYLOAD #
    ###########

    ...

    ##########
    # METHOD #
    ##########

    def get_counts(self, symbol, query_params=None, **kwargs):
        if not query_params:
            query_params = dict(symbol=symbol)
        resp = self.request.get(self.counts_url, query_params, **kwargs)
        return resp

    get_market = get_counts  # alias method
    get_pending = get_counts  # alias method

    ##########
    # SCHEMA #
    ##########
    @property
    def schema_get_counts(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "object",
                    "properties": {
                        "marketOrderCounts": {
                            "type": "number"
                        },
                        "pendingOrderCounts": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "marketOrderCounts",
                        "pendingOrderCounts"
                    ]
                }
            },
            "required": [
                "code",
                "result"
            ]
        }

    @property
    def schema_get_market(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "orderId": {
                                "type": "string"
                            },
                            "symbol": {
                                "type": "string"
                            },
                            "currency": {
                                "type": "string"
                            },
                            "volume": {
                                "type": "number"
                            },
                            "lotSize": {
                                "type": "number"
                            },
                            "lotSizeStep": {
                                "type": "number"
                            },
                            "minContractLotSize": {
                                "type": "number"
                            },
                            "swap": {
                                "type": "number"
                            },
                            "decimal": {
                                "type": "number"
                            },
                            "contractSize": {
                                "type": "number"
                            },
                            "units": {
                                "type": "number"
                            },
                            "unfilledVolume": {},
                            "openPrice": {
                                "type": "number"
                            },
                            "closePrice": {
                                "type": "number"
                            },
                            "currentPrice": {
                                "type": "number"
                            },
                            "priceTrigger": {},
                            "takeProfit": {
                                "type": "number"
                            },
                            "stopLoss": {
                                "type": "number"
                            },
                            "profit": {
                                "type": "number"
                            },
                            "tickSize": {
                                "type": "number"
                            },
                            "tickValue": {
                                "type": "number"
                            },
                            "commission": {},
                            "exchangeRate": {
                                "type": "number"
                            },
                            "marginMode": {
                                "type": "number"
                            },
                            "marginRate": {
                                "type": "number"
                            },
                            "marginPercentage": {
                                "type": "number"
                            },
                            "pointStep": {
                                "type": "number"
                            },
                            "indicate": {
                                "type": "string"
                            },
                            "exeMode": {
                                "type": "number"
                            },
                            "orderType": {
                                "type": "number"
                            },
                            "state": {
                                "type": "number"
                            },
                            "reason": {
                                "type": "number"
                            },
                            "tradeExpiry": {},
                            "fillPolicy": {
                                "type": "number"
                            },
                            "marketFillPolicy": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                }
                            },
                            "profitMode": {
                                "type": "number"
                            },
                            "comment": {
                                "type": "string"
                            },
                            "exitMethod": {},
                            "openTime": {
                                "type": "number"
                            },
                            "closeTime": {
                                "type": "number"
                            },
                            "expiration": {
                                "type": "number"
                            },
                            "isEnable": {
                                "type": "boolean"
                            },
                            "description": {},
                            "boughtQuantity": {},
                            "soldQuantity": {},
                            "avgBoughtPrice": {},
                            "avgSoldPrice": {},
                            "lastPrice": {},
                            "marketValue": {},
                            "pnlGross": {},
                            "symbolType": {},
                            "tickRulesGroup": {},
                            "tradable": {
                                "type": "boolean"
                            },
                            "editable": {
                                "type": "boolean"
                            },
                            "closable": {
                                "type": "boolean"
                            },
                            "trackable": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "orderId",
                            "symbol",
                            "currency",
                            "volume",
                            "lotSize",
                            "lotSizeStep",
                            "minContractLotSize",
                            "swap",
                            "decimal",
                            "contractSize",
                            "units",
                            "unfilledVolume",
                            "openPrice",
                            "closePrice",
                            "currentPrice",
                            "priceTrigger",
                            "takeProfit",
                            "stopLoss",
                            "profit",
                            "tickSize",
                            "tickValue",
                            "commission",
                            "exchangeRate",
                            "marginMode",
                            "marginRate",
                            "marginPercentage",
                            "pointStep",
                            "indicate",
                            "exeMode",
                            "orderType",
                            "state",
                            "reason",
                            "tradeExpiry",
                            "fillPolicy",
                            "marketFillPolicy",
                            "profitMode",
                            "comment",
                            "exitMethod",
                            "openTime",
                            "closeTime",
                            "expiration",
                            "isEnable",
                            "description",
                            "boughtQuantity",
                            "soldQuantity",
                            "avgBoughtPrice",
                            "avgSoldPrice",
                            "lastPrice",
                            "marketValue",
                            "pnlGross",
                            "symbolType",
                            "tickRulesGroup",
                            "tradable",
                            "editable",
                            "closable",
                            "trackable"
                        ]
                    }
                }
            },
            "required": [
                "code",
                "result"
            ]
        }

    @property
    def schema_get_pending(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "orderId": {
                                "type": "string"
                            },
                            "symbol": {
                                "type": "string"
                            },
                            "volume": {
                                "type": "number"
                            },
                            "lotSize": {
                                "type": "number"
                            },
                            "decimal": {
                                "type": "number"
                            },
                            "units": {
                                "type": "number"
                            },
                            "lotSizeStep": {
                                "type": "number"
                            },
                            "remainedLotSize": {
                                "type": "number"
                            },
                            "filledLotSize": {
                                "type": "number"
                            },
                            "minContractLotSize": {},
                            "openPrice": {},
                            "closePrice": {},
                            "currentPrice": {
                                "type": "number"
                            },
                            "price": {
                                "type": "number"
                            },
                            "takeProfit": {
                                "type": "number"
                            },
                            "stopLoss": {
                                "type": "number"
                            },
                            "profit": {},
                            "marginRate": {
                                "type": "number"
                            },
                            "indicate": {
                                "type": "string"
                            },
                            "exeMode": {
                                "type": "number"
                            },
                            "orderType": {
                                "type": "number"
                            },
                            "state": {
                                "type": "number"
                            },
                            "tradeExpiry": {
                                "type": "string"
                            },
                            "fillPolicy": {
                                "type": "number"
                            },
                            "marketFillPolicy": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                }
                            },
                            "comment": {
                                "type": "string"
                            },
                            "openTime": {
                                "type": "number"
                            },
                            "closeTime": {},
                            "expiration": {
                                "type": "number"
                            },
                            "isEnable": {
                                "type": "boolean"
                            },
                            "priceTrigger": {
                                "type": "number"
                            },
                            "description": {},
                            "lastPrice": {},
                            "limitPrice": {},
                            "stopPrice": {},
                            "symbolType": {},
                            "tickRulesGroup": {},
                            "horizonOrderStatus": {},
                            "unfilledVolume": {
                                "type": "number"
                            },
                            "id": {},
                            "tradable": {
                                "type": "boolean"
                            },
                            "editable": {
                                "type": "boolean"
                            },
                            "closable": {
                                "type": "boolean"
                            },
                            "trackable": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "orderId",
                            "symbol",
                            "volume",
                            "lotSize",
                            "decimal",
                            "units",
                            "lotSizeStep",
                            "remainedLotSize",
                            "filledLotSize",
                            "minContractLotSize",
                            "openPrice",
                            "closePrice",
                            "currentPrice",
                            "price",
                            "takeProfit",
                            "stopLoss",
                            "profit",
                            "marginRate",
                            "indicate",
                            "exeMode",
                            "orderType",
                            "state",
                            "tradeExpiry",
                            "fillPolicy",
                            "marketFillPolicy",
                            "comment",
                            "openTime",
                            "closeTime",
                            "expiration",
                            "isEnable",
                            "priceTrigger",
                            "description",
                            "lastPrice",
                            "limitPrice",
                            "stopPrice",
                            "symbolType",
                            "tickRulesGroup",
                            "horizonOrderStatus",
                            "unfilledVolume",
                            "id",
                            "tradable",
                            "editable",
                            "closable",
                            "trackable"
                        ]
                    }
                }
            },
            "required": [
                "code",
                "result"
            ]
        }
