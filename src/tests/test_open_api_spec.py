import pytest
from unittest.mock import patch, MagicMock
from contextlib import ExitStack

from app.open_api_spec import OpenApiSpec, Operation, get_operation, load_open_api_spec
from app.exceptions import HttpUnsupportedMediaTypeError


@pytest.mark.small
class TestOpenApiSpec:
    @pytest.mark.parametrize(
        "input, expected",
        [
            ("get", True),
            ("put", True),
            ("post", True),
            ("delete", True),
            ("options", True),
            ("head", True),
            ("patch", True),
            ("trace", True),
            (None, False),
            ("", False),
            ("aha", False),
        ],
    )
    def test_is_method(self, input, expected):
        assert OpenApiSpec.is_method(input) == expected

    def test_init(self):
        open_api_spec = OpenApiSpec()
        assert open_api_spec.file_path is None
        assert open_api_spec.openapi is None
        assert open_api_spec.info == {}
        assert open_api_spec.operations == {}

    def test_from_yaml_normal(self):
        patches = [
            {"target": "builtins.open"},
            {
                "target": "yaml.load",
                "return_value": {
                    "openapi": "3.0.1",
                    "info": {"version": "0.1.0"},
                    "paths": {
                        "/threads": {
                            # Content-Type なし
                            "get": {
                                "operationId": "get_threads",
                                "responses": {
                                    200: {
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/Threads"
                                                }
                                            }
                                        }
                                    }
                                },
                            },
                            # Content-Type 複数
                            "post": {
                                "operationId": "post_thread",
                                "requestBody": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Thread"
                                            }
                                        },
                                        "application/xml": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Thread"
                                            }
                                        },
                                    },
                                    "required": True,
                                },
                                "responses": {
                                    201: {"$ref": "#/components/responses/Thread"}
                                },
                            },
                        },
                        "/threads/{id}": {
                            # Content-Type 別のpath
                            "put": {
                                "operationId": "put_message",
                                "requestBody": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Thread"
                                            }
                                        }
                                    },
                                    "required": True,
                                },
                                "responses": {
                                    200: {"$ref": "#/components/responses/Thread"}
                                },
                            }
                        },
                    },
                },
            },
        ]

        with ExitStack() as stack:
            patchers = [stack.enter_context(patch(**item)) for item in patches]

            open_api_spec = OpenApiSpec()
            open_api_spec.from_yaml("/path/to/swagger_spec.yaml")

            assert open_api_spec.file_path == "/path/to/swagger_spec.yaml"
            assert open_api_spec.openapi == "3.0.1"
            assert open_api_spec.info == {"version": "0.1.0"}
            assert open_api_spec.operations == {
                "get_threads": Operation(
                    operation_id="get_threads",
                    path="/threads",
                    method="get",
                    media_types=[],
                ),
                "post_thread": Operation(
                    operation_id="post_thread",
                    path="/threads",
                    method="post",
                    media_types=["application/json", "application/xml"],
                ),
                "put_message": Operation(
                    operation_id="put_message",
                    path="/threads/{id}",
                    method="put",
                    media_types=["application/json"],
                ),
            }

            for patcher in patchers:
                patcher.assert_called_once()

    def test_from_yaml_exception(self):
        open_api_spec = OpenApiSpec()
        with pytest.raises(FileNotFoundError):
            open_api_spec.from_yaml("/path/to/swagger_spec.yaml")


@pytest.mark.small
class TestOperation:
    @pytest.mark.parametrize(
        "input, expected",
        [
            # OK
            (
                # input
                {
                    "operation": Operation(media_types=["application/json"]),
                    "media_type": "application/json",
                },
                # expected
                {"type": AssertionError},
            ),
            (
                # input
                {
                    "operation": Operation(media_types=[]),
                    "media_type": "application/json",
                },
                # expected
                {"type": AssertionError},
            ),
            # NG
            (
                # input
                {
                    "operation": Operation(media_types=["application/json"]),
                    "media_type": None,
                },
                # expected
                {
                    "type": HttpUnsupportedMediaTypeError,
                    "message": "Content-type required.",
                },
            ),
            (
                # input
                {
                    "operation": Operation(media_types=["application/json"]),
                    "media_type": "application/xml",
                },
                # expected
                {
                    "type": HttpUnsupportedMediaTypeError,
                    "message": "Content-type 'application/xml' not supported.",
                },
            ),
        ],
    )
    def test_validate_media_type(self, input, expected):
        operation = input["operation"]

        with pytest.raises(expected["type"]) as e:
            operation.validate_media_type(input["media_type"])
            # ↑でエラーにならなかったら、AssertionErrorを発生させる
            raise (AssertionError)

        if expected.get("message"):
            assert e.value.message == expected["message"]


@pytest.mark.small
def test_get_operation_normal():
    with patch("app.open_api_spec._open_api_spec_instance.get_operation") as patcher:
        get_operation("operation_found")
    patcher.assert_called_once()
    patcher.assert_called_with("operation_found")


@pytest.mark.small
def test_get_operation_exception():
    with pytest.raises(ValueError) as e:
        get_operation("operation_not_found")

    assert e.value.args == ("Operation 'operation_not_found' not found.",)


@pytest.mark.small
def test_load_open_api_spec():
    # appのモックを作成
    input = MagicMock()
    input.root_path = "/path/to"

    with patch("app.open_api_spec.OpenApiSpec.from_yaml") as patcher:
        load_open_api_spec(input)

        patcher.assert_called_once()
        patcher.assert_called_with(
            file_path=f"{input.root_path}/.settings/swagger_spec.yaml"
        )
