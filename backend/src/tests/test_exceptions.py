import pytest

from app.exceptions import HttpUnsupportedMediaTypeError


@pytest.mark.small
class TestHTTPError:
    def test_init(self):
        actual = HttpUnsupportedMediaTypeError("メッセージ")

        expected = {
            "message": "メッセージ",
            "status_code": 415,
            "status": "Unsupported Media Type",
            "errors": [],
        }
        assert actual.__dict__ == expected
