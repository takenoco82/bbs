import pytest

from app.api.schemas import ErrorInfo, Errors, ErrorsSchema


@pytest.mark.small
@pytest.mark.parametrize(
    "input, expected",
    [
        # 全項目あり
        (
            # input
            Errors(
                request_id="1a228e0a56e6ce80f15e6679be656dc2",
                status="Bad Request",
                message="Validation failed.",
                errors=[
                    ErrorInfo(code="コード1", field="項目1", description="説明1"),
                    ErrorInfo(code="コード2", field="項目2", description="説明2"),
                    ErrorInfo(),
                ],
            ),
            # expected
            {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Bad Request",
                "message": "Validation failed.",
                "errors": [
                    {"code": "コード1", "field": "項目1", "description": "説明1"},
                    {"code": "コード2", "field": "項目2", "description": "説明2"},
                    {"code": None, "field": None, "description": None},
                ],
            },
        ),
        # errors なし
        (
            # input
            Errors(
                request_id="1a228e0a56e6ce80f15e6679be656dc2",
                status="Bad Request",
                message="Validation failed.",
            ),
            # expected
            {
                "request_id": "1a228e0a56e6ce80f15e6679be656dc2",
                "status": "Bad Request",
                "message": "Validation failed.",
                "errors": [],
            },
        ),
        # 全項目なし
        (
            # input
            Errors(),
            # expected
            {"request_id": None, "status": None, "message": None, "errors": []},
        ),
    ],
)
def test_errors_schema_dump(input, expected):
    actual = ErrorsSchema().dump(input)
    assert actual == expected
