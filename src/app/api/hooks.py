import logging
import time

from flask import request, g


logger = logging.getLogger(__name__)


class BeforeRequestLog:
    def __init__(self, request):
        self.endpoint = f"{request.method} {request.url}"
        self.headers = {
            header_name: request.headers.get(header_name) for header_name in request.headers.keys()
        }

    @property
    def message(self):
        request_info = {"headers": self.headers}
        return f"{self.endpoint} is called. - {request_info}"


class AfterRequestLog:
    def __init__(self, request, response, process_time=None):
        self.endpoint = f"{request.method} {request.url}"
        self.status = response.status
        self.status_code = response.status_code
        self.operation_id = request.blueprint
        self.process_time = round(process_time, 6) if process_time else None

    @property
    def message(self):
        response_info = {
            "status_code": self.status_code,
            "operation_id": self.operation_id,
            "process_time": self.process_time,
        }
        return f"{self.endpoint} is finished. ({self.status}) - {response_info}"


def before_request_handlers():
    g.started_at = time.time()
    message = BeforeRequestLog(request).message
    logger.info(message)


def after_request_handlers(response):
    process_time = time.time() - g.started_at
    message = AfterRequestLog(request, response, process_time=process_time).message
    logger.info(message)
    return response


def teardown_request_handlers(response):
    return response


def teardown_appcontext_handlers(response):
    return response
