from src.routes.auth.login import Login
from src.routes.trade.market import Market
from src.routes.trade.order import Order
from src.routes.trade.pending import Pending


class TradeClient:
    def __init__(self, headers=None):
        if not headers:
            headers = Login().authenticate()
        self.market = Market(headers)
        self.order = Order(headers)
        self.pending = Pending(headers)
