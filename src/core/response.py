import functools
import json
import math
import operator
import re
from contextlib import suppress
from json import JSONDecodeError

import jsonschema

from src.consts import PASSED_ICON, FAILED_ICON
from src.utils.assert_utils import soft_assert, assert_log
from src.utils.logger_utils import logger


class XResponse:
    def __init__(self, resp):
        self._resp = resp

    def json(self, **kwargs):
        with suppress(JSONDecodeError):
            return self._resp.json(**kwargs)
        return {}

    def __getattr__(self, attr):
        return getattr(self._resp, attr)

    @property
    def time_in_second(self):
        return self._resp.elapsed.total_seconds()

    @property
    def request_headers(self):
        return dict(self._resp.request.headers)

    @property
    def headers(self):
        return dict(self._resp.headers)

    def check_status_code(self, expected):
        assert_log(
            actual=self._resp.status_code,
            expected=expected,
            msg=f"Verify status code {expected}",
            result=soft_assert(self._resp.status_code == expected)
        )

    def check_response_time(self, max_timeout=1):
        multiple = 10 ** 3
        actual = math.ceil(self.time_in_second * multiple) / multiple
        method = self._resp.request.method
        url = self._resp.request.path_url
        msg = f"Verify response time in seconds ({actual}s < {max_timeout}s) [ {method} {url} ]"
        time_unit = "s"
        if self.time_in_second < 1:
            max_timeout = 0.5
            msg = f"Verify response time in milliseconds ({int(actual * 1000)}ms < {int(max_timeout * 1000)}ms) [ {method} {url} ]"
            time_unit = "ms"

        assert_log(
            actual=actual,
            expected=max_timeout,
            msg=msg,
            result=soft_assert(actual <= max_timeout),
            time_unit=time_unit
        )

    def check_jsonschema(self, schema):
        msg = "Verify JSON schema"
        try:
            jsonschema.validate(instance=self._resp.json(), schema=schema)
            logger.info(f"{PASSED_ICON} {msg}")
        except jsonschema.ValidationError as e:
            logger.warning(f"{FAILED_ICON} {msg}")
            logger.warning(f"  JSON schema validation failed: {e.message} [{'.'.join([item for item in e.path])}]")
            soft_assert(False, msg)


    def __check_payload__(self, expected, *, key=None, ops, method):
        msg = "Verify payload"
        if key:
            msg += f" (Key: {key})"
            _path = map(lambda x: int(x) if x.isdigit() else x, filter(None, re.split(r'[\[.\]]', key)))
            try:
                actual = functools.reduce(operator.getitem, _path, self.json())
            except (IndexError, TypeError):
                actual = r"[~~missing-key-~~]"
        else:
            msg += " (Full payload)"
            actual = self.json()

        try:
            if ops == operator.contains and isinstance(actual, dict) and isinstance(expected, dict):
                res = actual.items() >= expected.items()
            else:
                res = ops(actual, expected)
        except Exception:
            res = False

        if isinstance(actual, dict):
            actual = json.dumps(actual, indent=4)

        if isinstance(expected, dict):
            expected = json.dumps(expected, indent=4)

        if soft_assert(res):
            msg = f"{PASSED_ICON} {msg}"
            printlog = logger.info
            printmsg = [msg, f"  [{method.upper()}] {expected}"]
        else:
            msg = f"{FAILED_ICON} {msg}"
            printlog = logger.warning
            printmsg = [msg, f"  [{method.upper()}] {expected} \t [Actual]: {actual}"]

        for _msg in printmsg:
            printlog(_msg)

    check_payload_equals = functools.partialmethod(__check_payload__, ops=operator.eq, method="equals")
    check_payload_not_equals = functools.partialmethod(__check_payload__, ops=operator.ne, method="not equals")
    check_payload_greater_than = functools.partialmethod(__check_payload__, ops=operator.gt, method="greater than")
    check_payload_less_than = functools.partialmethod(__check_payload__, ops=operator.lt, method="less than")
    check_payload_greater_equals = functools.partialmethod(__check_payload__, ops=operator.ge, method="greater or equals")
    check_payload_less_equals = functools.partialmethod(__check_payload__, ops=operator.le, method="less than or equals")
    check_payload_endswith = functools.partialmethod(__check_payload__, ops=lambda a, b: a.endswith(b), method="end with")
    check_payload_contains = functools.partialmethod(__check_payload__, ops=operator.contains, method="contains")
    check_payload_not_contains = functools.partialmethod(__check_payload__, ops=lambda a, b: b not in a, method="not contains")
    del __check_payload__

    def cash_request_to_curl(self):
        # Format request content
        method = self._resp.request.method.upper()
        lines = [f"curl --location --request {method} '{self._resp.request.url}'"]

        for key, value in self._resp.request.headers.items():
            lines.append(f"--header '{key}: {value}'")

        if self._resp.request.body and isinstance(self._resp.request.body, (str, bytes)):
            try:
                data = json.loads(self._resp.request.body)
                json_data = json.dumps(data)  # compact form

            except Exception:
                json_data = self._resp.request.body.decode() if isinstance(self._resp.request.body, bytes) else self._resp.request.body

            lines.append(f"--data-raw '{json_data}'")

        curl_command = " \n".join(lines)
        return curl_command
