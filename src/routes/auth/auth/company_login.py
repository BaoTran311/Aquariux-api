from src.core.request import XRequest
from src.data_runtime import DataRuntime
from src.routes.base_api import BaseAPI


class CompanyLogin(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = "/api/auth/v1/company/login"

    ### payload ###
    def required_payload(self, user_id, password, source):  # noqa
        return dict(
            source=source or "WEB",
            userId=user_id or DataRuntime.config.email,
            password=password or DataRuntime.config.password
        )

    ### method ###
    def post(self, payload, *, attach=True):
        resp = self.request.post(self.url, payload, attach=attach)
        return resp

    ### schema ###
    @property
    def schema(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string"
                        },
                        "user": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string"
                                },
                                "metatraderId": {
                                    "type": "string"
                                },
                                "metatraderGroup": {
                                    "type": "string"
                                },
                                "isDemo": {
                                    "type": "boolean"
                                },
                                "traderSubcription": {
                                    "type": "string"
                                },
                                "marketSubcription": {
                                    "type": "string"
                                },
                                "traderSubscription": {
                                    "type": "string"
                                },
                                "marketSubscription": {
                                    "type": "string"
                                },
                                "tenantId": {
                                    "type": "string"
                                },
                                "mainProductCode": {
                                    "type": "string"
                                },
                                "omsServerId": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source",
                                "metatraderId",
                                "metatraderGroup",
                                "isDemo",
                                "traderSubcription",
                                "marketSubcription",
                                "traderSubscription",
                                "marketSubscription",
                                "tenantId",
                                "mainProductCode",
                                "omsServerId",
                                "key_error"
                            ]
                        }
                    },
                    "required": [
                        "token",
                        "user"
                    ]
                }
            },
            "required": [
                "code",
                "result",
            ]
        }
