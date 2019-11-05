from flask import jsonify

from app.api.schemas import ErrorSchema


def validation_error_handler(error):
    errors = []
    for error_detail in error.args:
        for field in error_detail.keys():
            errors.append(
                {
                    "field": field,
                    "code": error_detail[field].get("code"),
                    "message": error_detail[field].get("message"),
                }
            )
    responseBody = {"errors": ErrorSchema(many=True).dump(errors)}
    return (jsonify(responseBody), 400)
