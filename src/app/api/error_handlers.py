import logging

from flask import jsonify, g
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from app.api.schemas import ErrorInfo, Errors, ErrorsSchema
from app.exceptions import HttpUnsupportedMediaTypeError


logger = logging.getLogger(__name__)


# 主に4xx系エラー (app.exceptions.HTTPError またはそれを継承したエラー) に対するハンドラー
def http_error_handler(error):
    data = Errors(
        request_id=g.request_id, status=error.status, message=error.message, errors=error.errors
    )
    response_body = ErrorsSchema().dump(data)
    return (jsonify(response_body), error.status_code)


# リクエストボディを検証した結果、NGだった場合のハンドラー
def validation_error_handler(error):
    from werkzeug.http import HTTP_STATUS_CODES

    logger.info("Validation failed.")

    errors = []
    for field in sorted(error.messages.keys()):
        messages = error.messages[field]
        for message in messages:
            # TODO codeは後で対応する
            errors.append(ErrorInfo(code=None, field=field, description=message))

    status_code = 400

    data = Errors(
        request_id=g.request_id,
        status=HTTP_STATUS_CODES.get(status_code),
        message="Validation failed.",
        errors=errors,
    )
    response_body = ErrorsSchema().dump(data)
    return (jsonify(response_body), status_code)


# Flaskのルーティングにマッチしなかった場合のハンドラー
def not_found_handler(error):
    data = Errors(request_id=g.request_id, status=error.name, message="Resource not found.")
    response_body = ErrorsSchema().dump(data)
    return (jsonify(response_body), error.code)


# 実行時例外が発生した場合のハンドラー
def application_error_handler(error):
    from werkzeug.http import HTTP_STATUS_CODES

    # stacktrace も出力する
    logger.exception(error)

    status_code = 500
    data = Errors(
        request_id=g.request_id,
        status=HTTP_STATUS_CODES.get(status_code),
        message="An unexpected error occurred.",
    )
    response_body = ErrorsSchema().dump(data)
    return (jsonify(response_body), status_code)


def register_error_handler(app):
    app.register_error_handler(HttpUnsupportedMediaTypeError, http_error_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(NotFound, not_found_handler)
    app.register_error_handler(Exception, application_error_handler)
