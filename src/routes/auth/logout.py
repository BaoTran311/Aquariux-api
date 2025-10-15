from src.consts import MULTI_OMS_CLIENTS
from src.core.request import XRequest
from src.data_runtime import DataRuntime
from src.enums.system import Clients, AccountType
from src.utils import Dotdict


class Logout:
    # def __new__(cls, headers=None, *args, **kwargs):
    #     instance = super().__new__(cls)
    #     url_map = Dotdict({
    #         Clients.LIRUNEX: {
    #             AccountType.CRM: "/auth/v1/company/login",
    #             AccountType.LIVE: "/auth/v2/company/live/login",
    #             AccountType.DEMO: "/auth/v2/company/demo/login"
    #         },
    #         Clients.TRANSACTCLOUD: {
    #             AccountType.LIVE: "/auth/v2/metatrader5/live/login",
    #             AccountType.DEMO: "/auth/v2/metatrader5/demo/login"
    #         }
    #     })
    #
    #     # select url based on client + handle external client
    #     default_client = Clients.LIRUNEX if DataRuntime.option.client in MULTI_OMS_CLIENTS else Clients.TRANSACTCLOUD
    #     instance.url = url_map.get(DataRuntime.config.client, url_map[default_client])[DataRuntime.option.account]
    #
    #     return instance

    def __init__(self, headers=None):
        self.request = XRequest(headers)
        self.logout_url = "/auth/v1/logout"

    ###########
    # PAYLOAD #
    ###########

    ...

    ##########
    # METHOD #
    ##########
    def post(self, **kwargs):
        resp = self.request.post(self.logout_url, None, **kwargs)
        return resp

    ##########
    # SCHEMA #
    ##########
    @property
    def success_schema(self):
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "result": {
                    "type": ["object", "null"]
                }
            },
            "required": [
                "code",
                "result"
            ]
        }
