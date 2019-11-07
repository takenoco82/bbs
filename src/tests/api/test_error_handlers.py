import pytest
from marshmallow import Schema, ValidationError, fields

from app.api import error_handlers
from run import app


class SampleSchema(Schema):
    field1 = fields.Str(required=True)


@pytest.mark.small
class TestErrorHandlers:
    def test_validation_error_handler(self):
        expetcted = {
            "status_code": 400,
            "body": {
                "errors": [
                    {
                        "field": "field1",
                        "code": None,
                        "message": "Missing data for required field.",
                    },
                ]
            },
        }

        with app.app_context():
            with pytest.raises(ValidationError) as e:
                schema = SampleSchema()
                schema.load({})

            actual = error_handlers.validation_error_handler(e.value)
            assert actual[1] == expetcted["status_code"]
            assert actual[0].json == expetcted["body"]
