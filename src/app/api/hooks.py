import logging
import time

from flask import request, g

from app.exceptions import HttpUnsupportedMediaTypeError


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
    g.request_id = request.headers.get("X-Request-Id", "")
    g.started_at = time.time()

    content_type = request.headers.get("Content-Type")
    if content_type and content_type != "application/json":
        raise HttpUnsupportedMediaTypeError(f"Content type '{content_type}' not supported.")

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


def configure_hooks(app):
    app.before_request(before_request_handlers)
    app.after_request(after_request_handlers)
    app.teardown_request(teardown_request_handlers)
    app.teardown_appcontext(teardown_appcontext_handlers)
