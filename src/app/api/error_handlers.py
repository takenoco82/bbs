import logging

from flask import jsonify

from app.api.schemas import ErrorSchema

logger = logging.getLogger(__name__)


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
