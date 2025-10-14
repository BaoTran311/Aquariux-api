from src.data_runtime import DataRuntime
from src.utils.logger_utils import logger

"""
Positive
"""


def test_positive_AUT_TC003_login_using_valid_DEMO_credential_with_required_params(auth_client):
    auth_sv = auth_client.login
    logger.info(f"- POST {auth_sv.url!r}")
    payload = auth_sv.required_payload()
    resp = auth_sv.post(payload)

    # Mandatory Checkpoints
    resp.check_status_code(200)
    resp.check_response_time(3)
    resp.check_jsonschema(auth_sv.success_schema)

    # Payload validation
    expect_user = {
        "source": "WEB",
        "isDemo": DataRuntime.is_demo(),
        "tenantId": DataRuntime.option.client,
        "metatraderId": f"{DataRuntime.config.user}"
    }
    resp.check_payload_contains(expect_user, key="result.user")


"""
Negative
"""


def test_negative_AUT_TC008_login_using_invalid_DEMO_credential_with_required_params(auth_client):
    auth_sv = auth_client.login
    expect_user = {
        "source": "WEB",
        "isDemo": True,
        "tenantId": "lirunex",
        "mainProductCode": "METATRADER5",
        "metatraderId": f"{DataRuntime.config.user}"
    }

    logger.info(f"- POST {auth_sv.url!r}")
    payload = auth_sv.required_payload("invalid user")
    resp = auth_sv.post(payload)

    # Mandatory Checkpoints
    resp.check_status_code(401)
    resp.check_response_time(1)
    resp.check_jsonschema(auth_sv.error_schema)

    # Payload validation
    resp.check_payload_equals("Invalid Login MetatraderId", key="message")
