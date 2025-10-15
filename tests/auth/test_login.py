from src.data_runtime import DataRuntime
from src.routes.auth.auth_client import AuthClient
from src.routes.auth.login import Login
from src.routes.auth.logout import Logout
from src.routes.trade.market import Market
from src.utils import assert_utils
from src.utils.logger_utils import logger

"""
Positive
"""


def test_positive_AUT_TC003_login_using_valid_DEMO_credential_with_required_params(auth_client):
    auth_sv = auth_client.login

    logger.info(f"- POST {auth_sv.login_url!r}")
    payload = auth_sv.required_payload()
    resp = auth_sv.post(payload)

    # Mandatory Checkpoints
    resp.check_status_code(200)
    resp.check_response_time(3)
    resp.check_jsonschema(auth_sv.success_schema)

    # Payload validation
    expect_data = {
        "source": "WEB",
        "isDemo": DataRuntime.is_demo(),
        "tenantId": DataRuntime.option.client,
        "metatraderId": f"{DataRuntime.config.user}"
    }
    resp.check_payload_contains(expect_data, key="result.user")


"""
Negative
"""


def test_negative_AUT_TC010_login_using_invalid_DEMO_credential_with_required_params(auth_client):
    auth_sv = auth_client.login

    logger.info(f"- POST {auth_sv.login_url!r}")
    payload = auth_sv.required_payload("invalid user")
    resp = auth_sv.post(payload)

    # Mandatory Checkpoints
    resp.check_status_code(401)
    resp.check_response_time(1)
    resp.check_jsonschema(auth_sv.error_schema)

    # Payload validation
    resp.check_payload_equals("Invalid Login MetatraderId", key="message")


"""
Integration
"""


def test_integration_AUT_TC019_user_cannot_reuse_old_token_after_logout():
    login_sv = Login()

    logger.info(f"Step 1: POST {login_sv.login_url}")
    payload = login_sv.required_payload()
    resp_login = login_sv.post(payload)
    resp_login.check_status_code(200)

    # Authenticate other service
    headers = dict(authorization=f"Bearer {resp_login.json()['result']['token']}")
    logout_sv = Logout(headers)
    market_sv = Market(headers)

    logger.info(f"Step 2: POST {logout_sv.logout_url}")
    resp_logout = logout_sv.post()
    resp_logout.check_status_code(200)

    logger.info(f"Step 3: GET {market_sv.symbols_all_url}")
    resp_symbols = market_sv.get_all_symbols()
    resp_symbols.check_status_code(401)
