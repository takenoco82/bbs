import logging

from flask import jsonify, g
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from app.api.schemas import Errors, ErrorSchema, ErrorsSchema
from app.exceptions import HttpUnsupportedMediaTypeError


logger = logging.getLogger(__name__)


def http_error_handler(error):
    data = Errors(
        request_id=g.request_id, status=error.status, message=error.message, errors=error.errors
    )
    response_body = ErrorsSchema().dump(data)
    return (jsonify(response_body), error.status_code)


def validation_error_handler(error):
    logger.info("validation error")

    errors = []
    for field in sorted(error.messages.keys()):
        messages = error.messages[field]
        for message in messages:
            errors.append(
                {
                    "field": field,
                    # TODO 後で対応する
                    "code": None,
                    "message": message,
                }
            )
    responseBody = {"errors": ErrorSchema(many=True).dump(errors)}
    return (jsonify(responseBody), 400)


def not_found_error_handler(error):
    errors = []
    errors.append(
        {
            "field": None,
            # TODO 後で対応する
            "code": None,
            "message": "Not Found.",
        }
    )
    responseBody = {"errors": ErrorSchema(many=True).dump(errors)}
    return (jsonify(responseBody), 404)


def application_error_handler(error):
    # stacktrace も出力する
    logger.exception(error)

    errors = []
    errors.append(
        {
            "field": None,
            # TODO 後で対応する
            "code": None,
            "message": "An unexpected error occurred",
        }
    )
    responseBody = {"errors": ErrorSchema(many=True).dump(errors)}
    return (jsonify(responseBody), 500)


def register_error_handler(app):
    app.register_error_handler(HttpUnsupportedMediaTypeError, http_error_handler)
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(NotFound, not_found_error_handler)
    app.register_error_handler(Exception, application_error_handler)
