import operator
from functools import partial

import pytest_check

from src.consts import PASSED_ICON, FAILED_ICON
from src.utils.logger_utils import logger


@pytest_check.check_func
def soft_assert(cond, msg=""):
    assert cond, msg


def assert_log(*, actual, expected, msg, result, time_unit=""):
    if time_unit == "ms":
        actual = int(actual * 1000)
        expected = int(expected * 1000)

    if result:
        printlog = logger.info
        icon = PASSED_ICON
    else:
        printlog = logger.warning
        icon = FAILED_ICON
        msg += f"""
               {'\t' * 3}  [Expected] : {expected}{time_unit}\t[Actual] : {actual}{time_unit}"""

    printlog(f"{icon} {msg}")


def __check_data__(actual, expected, message="", op_func=lambda a, b: a == b):
    if not message.startswith(("verify", "check")):
        message = f"Verify {message}"
    res = op_func(actual, expected)

    assert_log(
        actual=actual,
        expected=expected,
        msg=message,
        result=res,
    )


check_equals = partial(__check_data__, op_func=operator.eq)
check_not_equals = partial(__check_data__, op_func=operator.ne)
check_greater_than = partial(__check_data__, op_func=operator.gt)
check_greater_equal = partial(__check_data__, op_func=operator.ge)
check_less_than = partial(__check_data__, op_func=operator.lt)
check_less_equal = partial(__check_data__, op_func=operator.le)
check_contains = partial(__check_data__, op_func=operator.contains)
check_not_contains = partial(__check_data__, op_func=lambda a, b: b not in a)
del __check_data__
