from src.routes.auth.company_login import CompanyLogin


class AuthClient:
    def __init__(self, headers=None):
        self.company_login = CompanyLogin(headers)
