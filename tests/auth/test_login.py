from src.data_runtime import DataRuntime
from src.utils import Dotdict, assert_utils
from src.utils.logger_utils import logger


def test_negative_AUT_TC001_login_CRM_with_required_params(auth_client):
    sv = auth_client.login
    expect_user = {
        "source": "WEB",
        "isDemo": False,
        "tenantId": "lirunex",
        "mainProductCode": "METATRADER5",
        "omsServerId": "lirunex-oms-2"
    }

    logger.info(f"- Step 1: POST {sv.url!r} login")
    payload = Dotdict(sv.required_payload(
        DataRuntime.config.user, DataRuntime.config.password, "WEB",
    ))
    resp = sv.post(payload)
    resp.check_jsonschema(sv.schema)
    resp.check_status_code(400)
    resp.check_response_time(1)
    assert_utils.check_contains("This is sample test case", "test case")
    assert_utils.check_equals(1, 1, "1 = 1")
    # resp.check_payload_equals('200', key="code")


    # resp.check_payload_equals('WEB', key="code")
    # resp.check_payload_equals(payload['userId'], key="result.user.metatraderId")
    # resp.check_payload_not_equals(payload['userId'], key="result.user.metatraderId")
    # resp.check_payload_contains(expect_user, key="result.user")
    #
    # logger.info(f"- Step 2: POST {sv.url!r} without attach log to allure")
    # resp = sv.post(payload, attach=False)
    # resp.check_status_code(200)
    # resp.check_response_time(1)
    # resp.check_payload_equals('200', key="code")
    # resp.check_payload_equals(payload['userId'], key="result.user.metatraderId")
    # resp.check_payload_not_equals(payload['userId'], key="result.user.metatraderId")
    # resp.check_payload_contains(expect_user, key="result.user")
    #
    # logger.info("- Step 3: Update isDemo = True")
    # expect_user['isDemo'] = True
    # resp.check_payload_contains(expect_user, key="result.user")
