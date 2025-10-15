from src.routes.auth.login import Login
from src.routes.auth.logout import Logout


class AuthClient:
    def __init__(self, headers=None):
        if not headers:
            headers = Login().authenticate()
        self.login = Login()
        self.logout = Logout(headers)
