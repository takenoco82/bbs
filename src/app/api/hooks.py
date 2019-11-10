import logging

from flask import request


logger = logging.getLogger(__name__)


class BeforeRequestLog:
    def __init__(self, request):
        self.endpoint = f"{request.method} {request.url}"

    @property
    def message(self):
        return f"START - {self.endpoint} is called."


class AfterRequestLog:
    def __init__(self, request, response):
        self.endpoint = f"{request.method} {request.url}"
        self.status = response.status

    @property
    def message(self):
        return f"END - {self.endpoint} is finished. {self.status}"


def before_request_handlers():
    message = BeforeRequestLog(request).message
    logger.info(message)


def after_request_handlers(response):
    message = AfterRequestLog(request, response).message
    logger.info(message)
    return response


def teardown_request_handlers(response):
    return response


def teardown_appcontext_handlers(response):
    return response
