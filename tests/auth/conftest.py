import pytest

from src.routes.auth.auth_client import AuthClient


@pytest.fixture(scope="package")
def auth_client():
    return AuthClient()
