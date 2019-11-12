from unittest.mock import MagicMock

import pytest

from app.api.hooks import AfterRequestLog, BeforeRequestLog


@pytest.mark.small
class TestBeforeRequestLog:
    def test_message(self):
        input = {
            "method": "GET",
            "url": "http://example.com",
            "headers": {"Host": "example.com", "Accept": "applicatin/json"},
        }
        request = MagicMock(**input)

        actual = BeforeRequestLog(request).message
        expected = "GET http://example.com is called. - {}".format({"headers": input["headers"]})
        assert actual == expected


@pytest.mark.small
class TestAfterRequestLog:
    @pytest.mark.parametrize(
        "input, expected",
        [
            (
                {
                    "request": {
                        "method": "GET",
                        "url": "http://example.com",
                        "blueprint": "get_example",
                    },
                    "response": {"status_code": 200, "status": "200 OK"},
                    "process_time": None,
                },
                "GET http://example.com is finished. (200 OK) - {}".format(
                    {"status_code": 200, "operation_id": "get_example", "process_time": None}
                ),
            ),
            (
                {
                    "request": {
                        "method": "POST",
                        "url": "http://example.com",
                        "blueprint": "get_example",
                    },
                    "response": {"status_code": 201, "status": "201 CREATED"},
                    "process_time": 12.3456789,
                },
                "POST http://example.com is finished. (201 CREATED) - {}".format(
                    {"status_code": 201, "operation_id": "get_example", "process_time": 12.345679}
                ),
            ),
        ],
    )
    def test_message2(self, input, expected):
        request = MagicMock(**input["request"])
        response = MagicMock(**input["response"])

        actual = AfterRequestLog(request, response, process_time=input["process_time"]).message
        assert actual == expected
