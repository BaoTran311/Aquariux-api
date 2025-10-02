from src.data_runtime import DataRuntime
from src.routes.auth.auth_client import AuthClient
from src.utils import Dotdict
from src.utils.logger_utils import logger

sv = AuthClient.company_login


def test_positive_valid_credential():
    expect_user = {
        "source": "WEB",
        "isDemo": False,
        "tenantId": "lirunex",
        "mainProductCode": "METATRADER5",
        "omsServerId": "lirunex-oms-2"
    }
    logger.info(f"- Step 1: POST {sv.url!r}")
    payload = Dotdict(sv.required_payload(
        DataRuntime.config.email, DataRuntime.config.password, "WEB",
    ))
    resp = sv.post(payload)
    resp.check_jsonschema(sv.schema)
    resp.check_status_code(201)
    resp.check_response_time(1)
    resp.check_payload_equals('200', key="code")
    resp.check_payload_equals(payload['userId'], key="result.user.metatraderId")
    resp.check_payload_not_equals(payload['userId'], key="result.user.metatraderId")
    resp.check_payload_contains(expect_user, key="result.user")

    logger.info(f"- Step 2: POST {sv.url!r} without attach log to allure")
    resp = sv.post(payload, attach=False)
    resp.check_status_code(200)
    resp.check_response_time(2)

    logger.info("- Step 3: Update isDemo = True")
    expect_user['isDemo'] = True
    resp.check_payload_contains(expect_user, key="result.user")
