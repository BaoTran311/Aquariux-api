import pytest

from src.routes.auth.auth_client import AuthClient
from src.routes.market.market_client import MarketClient


@pytest.fixture(scope="package")
def market_client():
    return MarketClient()
