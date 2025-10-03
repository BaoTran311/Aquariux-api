from src.data_runtime import DataRuntime
from src.routes.auth.company_login import CompanyLogin
from src.routes.market.pending import Pending


class MarketClient:
    def __init__(self, headers=None):
        if not headers:
            headers = CompanyLogin().authenticate()
        self.pending = Pending(headers)
