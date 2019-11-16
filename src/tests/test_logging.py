from contextlib import ExitStack
from unittest.mock import MagicMock, patch

import pytest

from app.logging_config import LoggingConfig, init_logging_config


@pytest.mark.small
class TestLoggingConfig:
    def test_init(self):
        actual = LoggingConfig()
        expected = {"version": 1, "disable_existing_loggers": False}
        assert actual == expected

    def test_update_from_yaml_normal(self):
        patches = [
            {"target": "builtins.open"},
            {"target": "yaml.load", "return_value": {"root": {"level": "INFO"}}},
        ]

        with ExitStack() as stack:
            patchers = [stack.enter_context(patch(**item)) for item in patches]

            logging_config = LoggingConfig()
            logging_config.update_from_yaml("/path/to/logging.yaml")

            expected = {
                "version": 1,
                "disable_existing_loggers": False,
                "root": {"level": "INFO"},
            }

            assert logging_config == expected

            # patchしたメソッドが呼び出しされたかどうかの確認
            for patcher in patchers:
                patcher.assert_called_once()

    def test_update_from_yaml_exception(self):
        logging_config = LoggingConfig()
        with pytest.raises(FileNotFoundError):
            logging_config.update_from_yaml("/path/to/logging.yaml")


@pytest.mark.small
def test_init_logging_config():
    # app(Flaskのインスタンス)のモック
    input = MagicMock()
    input.root_path = "/path/to"

    patches = [
        {"target": "app.logging_config.LoggingConfig.update_from_yaml"},
        {"target": "logging.config.dictConfig"},
    ]

    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        init_logging_config(input)

        # app.logging_config.LoggingConfig.update_from_yaml() の呼び出し確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with("/path/to/.settings/logging.yaml")
        # logging.config.dictConfig() の呼び出し確認
        patchers[1].assert_called_once()
