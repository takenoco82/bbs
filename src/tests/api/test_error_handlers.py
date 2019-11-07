from unittest.mock import patch

import pytest
from marshmallow import Schema, ValidationError, fields

from app.api import error_handlers


class SampleSchema(Schema):
    field1 = fields.Str(required=True)
    field2 = fields.Str(required=True)


@pytest.mark.small
class TestErrorHandlers:
    @patch("app.api.error_handlers.jsonify")
    def test_validation_error_handler(self, patcher):
        expetcted = {
            "status_code": 400,
            "body": {
                "errors": [
                    {
                        "field": "field1",
                        "code": None,
                        "message": "Missing data for required field.",
                    },
                    {
                        "field": "field2",
                        "code": None,
                        "message": "Missing data for required field.",
                    }
                ]
            },
        }

        with pytest.raises(ValidationError) as e:
            schema = SampleSchema()
            schema.load({})

        actual = error_handlers.validation_error_handler(e.value)
        assert actual[1] == expetcted["status_code"]
        patcher.assert_called_once()
        patcher.assert_called_with(expetcted["body"])
