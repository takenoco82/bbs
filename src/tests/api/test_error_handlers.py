import pytest

from app.api import error_handlers
from run import app


@pytest.mark.small
class TestErrorHandlers:
    def test_validation_error_handler(self):
        with app.app_context():
            input = Exception(
                {
                    "field1": {
                        "code": "code1",
                        "message": "message1",
                    }
                },
            )
            expetcted = {
                "status_code": 400,
                "body": {
                    "errors": [
                        {
                            "field": "field1",
                            "code": "code1",
                            "message": "message1",
                        }
                    ]
                }
            }
            actual = error_handlers.validation_error_handler(input)
            assert actual[1] == expetcted["status_code"]
            assert actual[0].json == expetcted["body"]
