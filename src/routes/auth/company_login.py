from src.core.request import XRequest
from src.data_runtime import DataRuntime
from src.utils import Dotdict


class CompanyLogin:
    def __init__(self, headers=None):
        self.request = XRequest(headers)
        self.url = "/api/auth/v1/company/login"

    ### payload ###
    def required_payload(self, user_id, password, source="WEB"):  # noqa
        return dict(
            source=source.upper(),
            userId=user_id or DataRuntime.config.email,
            password=password or DataRuntime.config.password
        )

    ### method ###
    def post(self, payload, **kwargs):
        resp = self.request.post(self.url, payload, **kwargs)
        return resp

    def authenticate(self, user_id=None, password=None, source="WEB"):
        resp = self.post(self.required_payload(
            user_id or DataRuntime.config.email, password or DataRuntime.config.password, source),
            attach=False)
        assert resp.status_code == 200, f"Authentication failed with status code {resp.status_code}!!!"

        resp_data = Dotdict(resp.json())
        self.request.headers |= dict(userId=user_id, authorization=f"Bearer {resp_data.result.token}")
        return self.request.headers


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
