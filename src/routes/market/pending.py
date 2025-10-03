from src.core.request import XRequest


class Pending:
    def __init__(self, headers):
        self.request = XRequest(headers)
        self.url = "/api/order/v1/pending"

    ### method ###
    def get(self, params, **kwargs):
        resp = self.request.get(self.url, params, **kwargs)
        return resp

    ### schema ###
