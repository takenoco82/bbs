from unittest.mock import patch

import pytest
from marshmallow import Schema, ValidationError, fields

from app.api import error_handlers


class SampleSchema(Schema):
    field1 = fields.Str(required=True)
    field2 = fields.Str(required=True)


@pytest.mark.small
@patch("app.api.error_handlers.g")
@patch("app.api.error_handlers.logger")
@patch("app.api.error_handlers.jsonify")
def test_validation_error_handler(patcher1, patcher2, patcher3):
    patcher3.request_id = "1a228e0a56e6ce80f15e6679be656dc2"

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
    patcher1.assert_called_once()
    patcher1.assert_called_with(expetcted["body"])
