from flask import jsonify

from app.api.schemas import ErrorSchema


def validation_error_handler(error):
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
