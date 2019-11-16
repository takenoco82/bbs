from werkzeug.http import HTTP_STATUS_CODES


class HTTPError(Exception):
    def __init__(self, message, status_code, errors=None):
        self.message = message
        self.status_code = status_code
        self.status = HTTP_STATUS_CODES.get(self.status_code)
        self.errors = errors or []


class HttpUnsupportedMediaTypeError(HTTPError):
    def __init__(self, message):
        super().__init__(message, 415)
