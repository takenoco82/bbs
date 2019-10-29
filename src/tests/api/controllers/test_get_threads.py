from datetime import datetime, timezone
from unittest import mock

import pytest

from run import app


@pytest.mark.small
class TestGetThreads:
    client = app.test_client()
    url = "/threads"

    @pytest.mark.parametrize(("patcher", "expected"), [
        # データなし (0件)
        (
            # patcher
            {
                "target": "app.models.thread.Thread.find_list",
                "return_value": [],
            },
            # expected
            {
                "status_code": 200,
                "body": {
                    "threads": []
                }
            }
        ),
        # データあり (複数件)
        (
            # patcher
            {
                "target": "app.models.thread.Thread.find_list",
                "return_value": [
                    {
                        "id": "1",
                        "title": "title1",
                        "created_at": datetime(2019, 1, 2, 3, 4, 5, 123456, tzinfo=timezone.utc),
                        "updated_at": datetime(2020, 2, 3, 4, 5, 6, 234567, tzinfo=timezone.utc),
                    },
                    {
                        "id": "2",
                        "title": "title2",
                        "created_at": datetime(2021, 11, 12, 13, 14, 15, 0, tzinfo=timezone.utc),
                        "updated_at": datetime(2022, 12, 13, 14, 15, 16, 1, tzinfo=timezone.utc),
                    }
                ],
            },
            # expected
            {
                "status_code": 200,
                "body": {
                    "threads": [
                        {
                            "id": "1",
                            "title": "title1",
                            "created_at": "2019-01-02T03:04:05.123456+00:00",
                        },
                        {
                            "id": "2",
                            "title": "title2",
                            "created_at": "2021-11-12T13:14:15+00:00",
                        }
                    ]
                }
            }
        ),
    ])
    def test_2xx(self, patcher, expected):
        with mock.patch(patcher["target"], return_value=patcher["return_value"]):
            response = self.client.get(self.url)

            # status code
            assert response.status_code == expected["status_code"]
            # response body
            assert response.json == expected["body"]
