import base64
import binascii
import functools
import logging
import time
from contextlib import suppress

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
    parser.addoption("--client", default="lirunex", help="Client to run test (lirunex, transactCloud) - single value only")
    parser.addoption("--account", default="demo", choices=["live", "demo", "crm"], help="Account type to run test (lirunex: crm/ demo, transactCloud: live/ demo)")
    parser.addoption("--server", default="mt5", choices=["mt4", "mt5"], help="Server to run test on")
    parser.addoption("--user", help="Custom user used to run test")
    parser.addoption("--password", help="Raw custom password")
    parser.addoption("--url", help="Custom url for running external tenant")


def pytest_sessionstart(session):
    setup_logging(logging.INFO)

    logger.info("=== Start Pytest session ===")
    runtime_option = vars(session.config.option)

    if runtime_option["collectonly"]:  # count the total number of tests and then exit
        return

    # parse run test options
    client = runtime_option["client"]
    account_type = runtime_option["account"]
    server = runtime_option["server"]
    user = runtime_option["user"]
    password = runtime_option["password"]
    url = runtime_option["url"]

    # load env config file
    with open(consts.ENV_DIR / f"{runtime_option['env']}.yaml", "r") as _env:
        DataRuntime.config = Dotdict(yaml.load(_env, Loader=yaml.FullLoader))

    # load runtime option
    DataRuntime.option = Dotdict(runtime_option)

    # decode internal password
    with suppress(binascii.Error):
        DataRuntime.config[f"password_{account_type}"] = base64.b64decode(DataRuntime.config[f"password_{account_type}"]).decode()

    # assign config with runtime options
    DataRuntime.config.user = user or DataRuntime.config[client].credentials[server][f"user_{account_type}"]
    DataRuntime.config.password = password or DataRuntime.config[f"password_{account_type}"]
    DataRuntime.config.url = url or DataRuntime.config[client].url

    if runtime_option["debuglog"]:  # switch log level to debug
        setup_logging(logging.DEBUG)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    allure.dynamic.parent_suite(DataRuntime.option.client.upper())
    allure.dynamic.suite(DataRuntime.option.server.upper())

    print("\x00")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item: pytest.Item):
    allure.dynamic.tag(f"user: {DataRuntime.config.user}")


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


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    broken = len(terminalreporter.stats.get("broken", []))

    # terminalreporter.section("Summary")
    # tw = terminalreporter._tw  # terminal writer
    # tw.line(f"Total tests: {total}")
    # tw.line(f"Passed: {passed}", green=True)
    # tw.line(f"Failed: {failed + broken}", red=True)


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

            request_time = get_current_time()
            with suppress(KeyError):
                if not kwargs.pop("attach"):
                    request_time = None
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
