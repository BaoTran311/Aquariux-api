from src.routes.auth.login import Login


class AuthClient:
    def __init__(self, headers=None):
        self.login = Login(headers)
