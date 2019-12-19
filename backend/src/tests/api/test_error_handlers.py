from unittest.mock import patch
from contextlib import ExitStack

import pytest
from marshmallow import Schema, ValidationError, fields
from werkzeug.exceptions import NotFound

from app.api import error_handlers
from app.exceptions import HttpUnsupportedMediaTypeError


@pytest.mark.small
def test_http_error_handler():
    patches = [
        {"target": "app.api.error_handlers.jsonify"},
        {"target": "app.api.error_handlers.g"},
    ]

    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        # gにrequest_idを設定
        patchers[1].request_id = "1a228e0a56e6ce80f15e6679be656dc2"

        expetcted = {
            "status_code": 415,
            "body": {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Unsupported Media Type",
                "message": "aha",
                "errors": [],
            },
        }

        actual = error_handlers.http_error_handler(HttpUnsupportedMediaTypeError("aha"))

        assert actual[1] == expetcted["status_code"]
        # レスポンスボディの検証: jsonify()への引数で確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with(expetcted["body"])


@pytest.mark.small
def test_validation_error_handler():
    class SampleSchema(Schema):
        field1 = fields.Str(required=True)
        field2 = fields.Str(required=True)

    patches = [
        {"target": "app.api.error_handlers.jsonify"},
        {"target": "app.api.error_handlers.g"},
        {"target": "app.api.error_handlers.logger"},
    ]

    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        # gにrequest_idを設定
        patchers[1].request_id = "1a228e0a56e6ce80f15e6679be656dc2"

        expetcted = {
            "status_code": 400,
            "body": {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Bad Request",
                "message": "Validation failed.",
                "errors": [
                    {
                        "field": "field1",
                        "code": None,
                        "description": "Missing data for required field.",
                    },
                    {
                        "field": "field2",
                        "code": None,
                        "description": "Missing data for required field.",
                    },
                ],
            },
        }

        with pytest.raises(ValidationError) as e:
            schema = SampleSchema()
            schema.load({})

        actual = error_handlers.validation_error_handler(e.value)

        assert actual[1] == expetcted["status_code"]
        # レスポンスボディの検証: jsonify()への引数で確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with(expetcted["body"])

        # ログの検証: logger.info()への引数で確認
        patchers[2].info.assert_called_once()
        patchers[2].info.assert_called_with("Validation failed.")


@pytest.mark.small
def test_not_found_handler():
    patches = [
        {"target": "app.api.error_handlers.jsonify"},
        {"target": "app.api.error_handlers.g"},
        {"target": "app.api.error_handlers.logger"},
    ]

    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        # gにrequest_idを設定
        patchers[1].request_id = "1a228e0a56e6ce80f15e6679be656dc2"

        expetcted = {
            "status_code": 404,
            "body": {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Not Found",
                "message": "Endpoint not found.",
                "errors": [],
            },
        }

        actual = error_handlers.not_found_handler(NotFound())

        assert actual[1] == expetcted["status_code"]
        # レスポンスボディの検証: jsonify()への引数で確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with(expetcted["body"])

        # ログの検証: logger.info()への引数で確認
        patchers[2].info.assert_called_once()
        patchers[2].info.assert_called_with("Endpoint not found.")


@pytest.mark.small
def test_application_error_handler():
    patches = [
        {"target": "app.api.error_handlers.jsonify"},
        {"target": "app.api.error_handlers.g"},
        {"target": "app.api.error_handlers.logger"},
    ]

    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        # gにrequest_idを設定
        patchers[1].request_id = "1a228e0a56e6ce80f15e6679be656dc2"

        expetcted = {
            "status_code": 500,
            "body": {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Internal Server Error",
                "message": "An unexpected error occurred.",
                "errors": [],
            },
        }

        err = ValueError("aha")
        actual = error_handlers.application_error_handler(err)

        assert actual[1] == expetcted["status_code"]
        # レスポンスボディの検証: jsonify()への引数で確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with(expetcted["body"])

        # ログの検証: logger.exception()への引数で確認
        patchers[2].exception.assert_called_once()
        patchers[2].exception.assert_called_with(err)
