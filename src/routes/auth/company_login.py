from src.consts import MULTI_OMS_CLIENTS
from src.core.request import XRequest
from src.data_runtime import DataRuntime
from src.enums.system import Clients, AccountType
from src.utils import Dotdict


class CompanyLogin:
    def __new__(cls, headers=None, *args, **kwargs):
        instance = super().__new__(cls)
        url_map = Dotdict({
            Clients.LIRUNEX: {
                AccountType.CRM: "/api/auth/v1/company/login",
                AccountType.LIVE: "/api/auth/v2/company/live/login",
                AccountType.DEMO: "/api/auth/v2/company/demo/login"
            },
            Clients.TRANSACTCLOUD: {
                AccountType.LIVE: "/api/auth/v2/metatrader5/live/login",
                AccountType.DEMO: "/api/auth/v2/metatrader5/demo/login"
            }
        })

        # select url based on client + handle external client
        default_client = Clients.LIRUNEX if DataRuntime.option.client in MULTI_OMS_CLIENTS else Clients.TRANSACTCLOUD
        instance.url = url_map.get(DataRuntime.config.client, url_map[default_client])[DataRuntime.option.account]

        return instance


    def __init__(self, headers=None):
        self.request = XRequest(headers)

    ### payload ###
    def required_payload(self, user_id, password, source="WEB"):  # noqa
        return dict(
            source=source.upper(),
            userId=user_id or DataRuntime.config.user,
            password=password or DataRuntime.config.password
        )

    ### method ###
    def post(self, payload, **kwargs):
        resp = self.request.post(self.url, payload, **kwargs)
        return resp

    def authenticate(self, user_id=None, password=None, source="WEB"):
        resp = self.post(self.required_payload(user_id, password, source), attach=False)
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
