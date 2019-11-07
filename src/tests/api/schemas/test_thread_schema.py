from datetime import datetime
from unittest.mock import patch
from uuid import UUID

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.api.schemas import ThreadSchema
from app.models import Thread


@pytest.mark.small
class TestThreadSchema:
    # load 正常系
    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            (
                {"title": "タイトル1"},
                {
                    "id": "add96e80-fb11-11e9-bc1d-0242ac170003",
                    "title": "タイトル1",
                    "created_at": datetime(2019, 1, 2, 12, 34, 56, 123456),
                    "updated_at": datetime(2019, 1, 2, 12, 34, 56, 123456),
                },
            ),
        ],
    )
    @patch("uuid.uuid4", return_value=UUID("add96e80-fb11-11e9-bc1d-0242ac170003"))
    @freeze_time("2019-01-02 12:34:56.123456")
    def test_load_normal(self, patcher, input, expected):
        schema = ThreadSchema()

        actual = schema.load(input)
        expected = Thread(**expected)

        assert patcher.called
        assert actual.__repr__() == expected.__repr__()

    # load(validate)
    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            # 正常系
            (
                {"title": "タイトル1"},
                {
                    "type": AssertionError,
                }
            ),
            # 項目なし
            (
                {},
                {
                    "type": ValidationError,
                    "messages": {
                        "title": ["Missing data for required field."],
                    }
                }
            ),
            # null
            (
                {"title": None},
                {
                    "type": ValidationError,
                    "messages": {
                        "title": ["Field may not be null."],
                    }
                }
            ),
            # under min length
            (
                {"title": ""},
                {
                    "type": ValidationError,
                    "messages": {
                        "title": ["Length must be between 1 and 128."],
                    }
                }
            ),
            # 対象外の項目
            (
                {
                    "id": "add96e80-fb11-11e9-bc1d-0242ac170001",
                    "title": "タイトル1"
                },
                {
                    "type": ValidationError,
                    "messages": {
                        "id": ["Unknown field."]
                    }
                }
            )
        ],
    )
    @patch("uuid.uuid4", return_value=UUID("add96e80-fb11-11e9-bc1d-0242ac170003"))
    @freeze_time("2019-01-02 12:34:56.123456")
    def test_load_validate(self, patcher, input, expected):
        schema = ThreadSchema()

        with pytest.raises(expected["type"]) as e:
            schema.load(input)
            # validate(load)の結果、何も問題がない場合のみ、ここまでくる
            raise AssertionError("ok")

        if expected.get("messages"):
            assert e.value.messages == expected.get("messages")
