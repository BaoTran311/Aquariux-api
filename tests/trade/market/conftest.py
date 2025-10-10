import pytest

from src.routes.trade.trade_client import TradeClient


@pytest.fixture(scope="package")
def trade_client():
    return TradeClient()
