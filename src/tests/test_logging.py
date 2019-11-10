from contextlib import ExitStack
from unittest.mock import patch

import pytest

from app.logging import Logging


@pytest.mark.small
class TestLogging:
    def test_init(self):
        obj = Logging(logging_config_file="/path/to/logging.yaml")
        assert obj.logging_config_file == "/path/to/logging.yaml"

    @pytest.mark.parametrize(
        "patches, input, expected",
        [
            # logging_config_file なし
            (
                # patches
                [],
                # input
                {"logging_config_file": None},
                # expected
                {"version": 1, "disable_existing_loggers": False},
            ),
            # logging_config_file が存在しない
            (
                # patches
                [],
                # input
                {"logging_config_file": "/path/to/logging.yaml"},
                # expected
                {"version": 1, "disable_existing_loggers": False},
            ),
            # logging_config_file が存在する
            (
                # patches
                [
                    {"target": "builtins.open"},
                    {"target": "yaml.load", "return_value": {"root": {"level": "INFO"}}},
                ],
                # input
                {"logging_config_file": "/workspace/src/logging.yaml"},
                # expected
                {"version": 1, "disable_existing_loggers": False, "root": {"level": "INFO"}},
            ),
        ],
    )
    def test_config(self, patches, input, expected):
        with ExitStack() as stack:
            patchers = [stack.enter_context(patch(**item)) for item in patches]

            obj = Logging(logging_config_file=input["logging_config_file"])
            assert obj.config == expected

            for patcher in patchers:
                patcher.assert_called_once()
