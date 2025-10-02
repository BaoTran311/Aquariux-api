from src.routes.base_api import BaseAPI


class Company(BaseAPI):
    def __init__(self):
        super().__init__()
        self._url = "/api/config/v1/company"

    def get(self, params=None):
        resp = self.request.get(self._url, params)
        return resp
