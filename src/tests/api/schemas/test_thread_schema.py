import pytest
from marshmallow import ValidationError

from app.api.schemas import ThreadSchema
from app.models import Thread


@pytest.mark.small
class TestThreadSchema:
    # load 正常系
    @pytest.mark.parametrize(
        ("input", "expected"), [({"title": "タイトル1"}, {"title": "タイトル1"})]
    )
    def test_load_normal(self, input, expected):
        schema = ThreadSchema()

        actual = schema.load(input)
        expected = Thread(**expected)

        assert actual.__repr__() == expected.__repr__()

    # load(validate)
    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            # 正常系 min length
            ({"title": "1"}, {"type": AssertionError}),
            # 正常系 max length
            (
                {
                    "title": (
                        "タイトル5678901234567890123456789012345678901234567890"
                        "12345678901234567890123456789012345678901234567890"
                        "1234567890123456789012345678"
                    )
                },
                {"type": AssertionError},
            ),
            # 項目なし
            (
                {},
                {
                    "type": ValidationError,
                    "messages": {"title": ["Missing data for required field."]},
                },
            ),
            # null
            (
                {"title": None},
                {
                    "type": ValidationError,
                    "messages": {"title": ["Field may not be null."]},
                },
            ),
            # under min length
            (
                {"title": ""},
                {
                    "type": ValidationError,
                    "messages": {"title": ["Length must be between 1 and 128."]},
                },
            ),
            # over max length
            (
                {
                    "title": (
                        "12345678901234567890123456789012345678901234567890"
                        "12345678901234567890123456789012345678901234567890"
                        "12345678901234567890123456789"
                    )
                },
                {
                    "type": ValidationError,
                    "messages": {"title": ["Length must be between 1 and 128."]},
                },
            ),
            # invalid type
            (
                {"title": 1234},
                {
                    "type": ValidationError,
                    "messages": {"title": ["Not a valid string."]},
                },
            ),
            # 対象外の項目
            (
                {"id": "add96e80-fb11-11e9-bc1d-0242ac170001", "title": "タイトル1"},
                {"type": ValidationError, "messages": {"id": ["Unknown field."]}},
            ),
        ],
    )
    def test_load_validate(self, input, expected):
        schema = ThreadSchema()

        with pytest.raises(expected["type"]) as e:
            schema.load(input)
            # validate(load)の結果、何も問題がない場合のみ、ここまでくる
            raise AssertionError("ok")

        if expected.get("messages"):
            assert e.value.messages == expected.get("messages")
