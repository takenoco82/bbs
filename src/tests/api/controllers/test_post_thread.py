from contextlib import ExitStack
from datetime import datetime, timezone
from unittest.mock import patch
from uuid import UUID

import pytest
from freezegun import freeze_time

from app.models import Thread
from run import app


@pytest.mark.small
class TestPostThread:
    client = app.test_client()
    url = "/threads"

    # リクエストボディ → modelへの変換
    @pytest.mark.parametrize(
        ("patches", "input", "expected"),
        [
            (
                # patches
                [
                    {
                        "target": "app.api.schemas.ThreadSchema.load",
                        "return_value": Thread(title="タイトル1"),
                    },
                    {
                        "target": "app.models.thread.Thread.save"
                    },
                ],
                # input
                {
                    "headers": {"Content-Type": "application/json"},
                    "body": {"title": "タイトル1"}
                },
                # expected
                {
                    "status_code": 201
                },
            )
        ],
    )
    def test_deserialize(self, patches, input, expected):
        with ExitStack() as stack:
            patchers = [stack.enter_context(patch(**item)) for item in patches]

            response = self.client.post(
                self.url, headers=input.get("headers"), json=input.get("body")
            )

            # status code
            assert response.status_code == expected["status_code"]

            # patch の確認 (デシリアライズで適切な引数を渡せているか)
            patchers[0].assert_called_once()
            patchers[0].assert_called_with(input["body"])

    # レスポンス
    @pytest.mark.parametrize(
        ("patches", "input", "expected"),
        [
            # 2xx
            (
                # patches
                [
                    {
                        "target": "uuid.uuid4",
                        "return_value": UUID("add96e80-fb11-11e9-bc1d-0242ac170003"),
                    },
                    {
                        "target": "app.models.thread.Thread.save"
                    },
                ],
                # input
                {
                    "headers": {"Content-Type": "application/json"},
                    "body": {"title": "タイトル1"}
                },
                # expected
                {
                    "status_code": 201,
                    "body": {
                        "id": "add96e80-fb11-11e9-bc1d-0242ac170003",
                        "title": "タイトル1",
                        "created_at": "2019-11-07T12:34:56.123456+00:00",
                    },
                },
            ),
            # 400
            (
                # patches
                [
                    # model変換時に ValidationErrorが発生して、ここまで到達しない
                    # {
                    #     "target": "uuid.uuid4",
                    #     "return_value": UUID("add96e80-fb11-11e9-bc1d-0242ac170003"),
                    # },
                    # {
                    #     "target": "app.models.thread.Thread.save"
                    # },
                ],
                # input
                {
                    "headers": {"Content-Type": "application/json"},
                    "body": {},
                },
                # expected
                {
                    "status_code": 400
                },
            ),
        ],
    )
    @freeze_time("2019-11-07 12:34:56.123456")
    def test_response(self, patches, input, expected):
        with ExitStack() as stack:
            patchers = [stack.enter_context(patch(**item)) for item in patches]

            response = self.client.post(
                self.url, headers=input.get("headers"), json=input.get("body")
            )

            # status code
            assert response.status_code == expected["status_code"]
            # response body
            if expected.get("body"):
                assert response.get_json() == expected["body"]

            # patch
            for patcher in patchers:
                patcher.assert_called_once()

    # modelへの引数
    @pytest.mark.parametrize(
        ("patches", "input", "expected"),
        [
            (
                # patches
                [
                    {
                        "target": "uuid.uuid4",
                        "return_value": UUID("add96e80-fb11-11e9-bc1d-0242ac170003"),
                    },
                    {
                        "target": "app.models.thread.Thread.save"
                    },
                ],
                # input
                {
                    "headers": {"Content-Type": "application/json"},
                    "body": {"title": "タイトル1"}
                },
                # expected
                {
                    "status_code": 201,
                    "thread": {
                        "id": "add96e80-fb11-11e9-bc1d-0242ac170003",
                        "title": "タイトル1",
                        "created_at": datetime(
                            2019, 11, 7, 12, 34, 56, 123456, tzinfo=timezone.utc
                        ),
                        "updated_at": datetime(
                            2019, 11, 7, 12, 34, 56, 123456, tzinfo=timezone.utc
                        ),
                    },
                },
            )
        ],
    )
    @freeze_time("2019-11-07 12:34:56.123456")
    def test_model_params(self, patches, input, expected):
        with ExitStack() as stack:
            patcher = [stack.enter_context(patch(**item)) for item in patches]

            response = self.client.post(self.url, headers=input["headers"], json=input["body"])

            # status code
            assert response.status_code == expected["status_code"]

            # ホントは assert_called_with() でやりたいけど、SQLAlchemy の model がいい感じに比較できないので
            # call_args から呼び出し時の引数を取得して、それで比較する

            # patch
            thread_save = patcher[1]
            # 引数の数
            thread_save_args = thread_save.call_args[0]
            assert len(thread_save_args) == 1
            # 引数の内容
            assert thread_save_args[0].__repr__() == Thread(**expected["thread"]).__repr__()
