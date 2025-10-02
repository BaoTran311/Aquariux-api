import base64
import binascii
import functools
import json
import logging
import textwrap
import time
from contextlib import suppress
from pathlib import Path

import allure
import pytest
import requests
import yaml

from src import consts
from src.core.response import XResponse
from src.data_runtime import DataRuntime
from src.utils import Dotdict
from src.utils.allure_utils import custom_log_info, custom_log_warning, delete_container_files, custom_allure_result, attach_request_response, \
    format_request_response
from src.utils.datetime_utils import pretty_time, get_current_time
from src.utils.logger_utils import setup_logging, logger

_loggingmsgs = []


def pytest_addoption(parser):
    general = parser.getgroup("General")
    general.addoption("--debuglog", action="store_true", default=False)
    parser.addoption("--env", default="sit", help="Environment to run tests (sit, release_sit, uat)")
    parser.addoption("--client", default="lirunex", help="Client to test (lirunex, transactCloud) - single value only")


def pytest_sessionstart(session):
    setup_logging(logging.INFO)

    logger.info("=== Start Pytest session ===")
    runtime_option = vars(session.config.option)

    if runtime_option["collectonly"]:  # count the total number of tests and then exit
        return

    with open(consts.ENV_DIR / f"{runtime_option['env']}.yaml", "r") as _env:
        DataRuntime.config = Dotdict(yaml.load(_env, Loader=yaml.FullLoader))
    DataRuntime.option = Dotdict(runtime_option)

    with suppress(binascii.Error):
        DataRuntime.config.password = base64.b64decode(DataRuntime.config.password).decode()

    if runtime_option["debuglog"]:  # switch log level to debug
        setup_logging(logging.DEBUG)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    print("\x00")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item: pytest.Item):
    print("\x00")
    del _loggingmsgs[:]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global _loggingmsgs
    report = (yield).get_result()

    if report.when == 'call':
        allure.dynamic.description_html(''.join(_loggingmsgs))


def pytest_runtest_logreport(report):
    if report.when == "call":
        printlog = logger.info if report.outcome == "passed" else logger.warning
        print("\x00")  # print a non-printable character to break a new line on console
        printlog("---------------")  # noqa
        printlog(f"Test case     | {report.nodeid}")  # noqa
        printlog(f"Test duration | {pretty_time(report.duration)}")  # noqa
        printlog("---------------")


def pytest_sessionfinish(session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.info("=== End tests session ===")

    if vars(session.config.option)["collectonly"]:
        return

    allure_dir = session.config.option.allure_report_dir
    if not allure_dir:
        return

    # Delete container files
    delete_container_files(allure_dir)

    custom_allure_result(allure_dir)


@pytest.fixture(scope="session", autouse=True)
def patch_logger(request):
    global _loggingmsgs

    def patch_info(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True

            _logmsgs, *_ = args
            _loggingmsgs.append(custom_log_info(_logmsgs))

            return f(*args, **kwargs)

        return wrapper

    def patch_warning(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True

            _logmsgs, *_ = args
            _loggingmsgs.append(custom_log_warning(_logmsgs))

            return f(*args, **kwargs)

        return wrapper

    logger.info = patch_info(logger.info)
    logger.warning = patch_warning(logger.warning)


@pytest.fixture(scope="session", autouse=True)
def patch_request(request):
    def patch(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True

            request_time = not kwargs.pop("attach") or get_current_time()
            result = XResponse(f(*args, **kwargs))
            logger.debug(format_request_response(result))

            if isinstance(request_time, str):
                attach_request_response(result, request_time=request_time)

            return result

        return wrapper

    requests.Session.request = patch(requests.Session.request)


@pytest.fixture(scope="session", autouse=True)
def avoid_timeout():
    def patch(f):
        @functools.wraps(f)
        def handler(*args, **kwargs):
            _retries = 3
            _polling = 5

            for _ in range(_retries):
                try:
                    return f(*args, **kwargs)
                except (requests.exceptions.ConnectTimeout,
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.ConnectionError):
                    time.sleep(_polling)

            return f(*args, **kwargs)

        return handler

    requests.Session.request = patch(requests.Session.request)
