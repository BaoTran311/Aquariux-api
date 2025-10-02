from src.routes.base_api import BaseAPI
from src.utils import Dotdict


class Login(BaseAPI):
    def __init__(self):
        super().__init__()
        # self._url = "/api/auth/v2/company/demo/auth"
        self.deprecated_url = "/api/auth/v2/company/demo/login"
        self._url = "/api/auth/v3/company/demo/login"

    # define payload
    def required_payload(self, user_id, password):  # noqa
        return dict(
            source="WEB", userId=user_id or "2092009632", password=password or "Autotest@12345"
        )


    def authenticate(self, user_id=None, password=None):
        payload = {
            "source": "WEB",
            "password": password or "Autotest@12345",
            "userId": user_id or "2092009632"
        }
        resp = self.request.post(
            self._url, json=payload, attach=False
        )
        assert resp.status_code == 200, f"Authentication failed with status code {resp.status_code}!!!"

        resp_data = Dotdict(resp.json())
        self.request.headers |= dict(authorization=f"Bearer {resp_data.result.token}")
