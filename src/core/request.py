import functools

import requests

from src.core.response import XResponse
from src.data_runtime import DataRuntime
from src.utils.logger_utils import logger


def __catcherror__(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        __tracebackhide__ = True
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError) as error:
            logger.warning("=" * 32)
            logger.warning(f"| Name    : {type(error).__name__}")
            logger.warning(f"| Error   : {error}")

    return wrapper


class XRequest:
    def __init__(self):
        self.headers = {}
        self.endpoint = DataRuntime.config.url[DataRuntime.option.client]

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @__catcherror__
    def get(self, url: str, query_param=None, **kwargs):
        params = {
            "headers": kwargs.get("headers") or self.headers,
            "params": query_param,
            **kwargs
        }
        resp = XResponse(requests.get(url=f"{self.endpoint}{url}", **params))
        return resp

    @__catcherror__
    def post(self, url: str, payload, **kwargs):
        resp = XResponse(requests.post(url=f"{self.endpoint}{url}", json=payload, **kwargs))
        return resp

    @__catcherror__
    def put(self, url: str, payload, **kwargs):
        resp = XResponse(requests.put(url=f"{self.endpoint}{url}", json=payload, **kwargs))
        return resp

    @__catcherror__
    def patch(self, url: str, payload, **kwargs):
        resp = XResponse(requests.patch(url=f"{self.endpoint}{url}", json=payload, **kwargs))
        return resp

    @__catcherror__
    def delete(self, url: str, query_param=None, **kwargs):
        resp = XResponse(requests.delete(url=f"{self.endpoint}{url}", params=query_param, **kwargs))
        return resp
