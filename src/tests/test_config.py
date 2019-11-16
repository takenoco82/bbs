from unittest.mock import MagicMock, patch
from contextlib import ExitStack

import pytest

from app.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    init_app_config,
)


@pytest.mark.small
class TestConfig:
    environment_variables = {
        "MYSQL_USER": "scott",
        "MYSQL_PASSWORD": "tiger",
        "MYSQL_HOST": "localhost",
        "MYSQL_DATABASE": "world",
    }

    @pytest.fixture
    def mock_env_setting(self, monkeypatch):
        for key, value in self.environment_variables.items():
            monkeypatch.setenv(key, value)

    @pytest.fixture
    def mock_env_missing(self, monkeypatch):
        for key in self.environment_variables.keys():
            monkeypatch.delenv(key, raising=False)

    def test_sqlalchemy_database_uri_env_setting(self, mock_env_setting):
        actual = Config().SQLALCHEMY_DATABASE_URI
        expected = "mysql+pymysql://scott:tiger@localhost:3306/world?charset=utf8mb4"
        assert actual == expected

    def test_sqlalchemy_database_uri_env_missing(self, mock_env_missing):
        actual = Config().SQLALCHEMY_DATABASE_URI
        expected = "mysql+pymysql://admin:admin@db:3306/bbs?charset=utf8mb4"
        assert actual == expected


@pytest.mark.small
@pytest.mark.parametrize(
    "input, expected",
    [
        (None, ProductionConfig),
        ("production", ProductionConfig),
        ("development", DevelopmentConfig),
        ("test", TestingConfig),
    ],
)
def test_get_config_object(monkeypatch, input, expected):
    from app.config import get_config_object

    if input:
        monkeypatch.setenv("BBS_APP_CONFIG", input)
        config_obj = get_config_object()
        assert isinstance(config_obj, expected)
    else:
        monkeypatch.delenv("BBS_APP_CONFIG", raising=False)
        config_obj = get_config_object()
        assert isinstance(config_obj, expected)


@pytest.mark.small
def test_init_app_config():
    patches = [
        {"target": "app.config.load_open_api_spec"},
    ]
    with ExitStack() as stack:
        patchers = [stack.enter_context(patch(**item)) for item in patches]

        # app(Flaskインスタンス)のモック
        input = MagicMock()
        input.root_path = "/path/to"

        init_app_config(input)

        # app.config.from_object() の呼び出しの確認
        input.config.from_object.assert_called_once()
        # app.open_api_spec.load_open_api_spec() の呼び出しの確認
        patchers[0].assert_called_once()
        patchers[0].assert_called_with(
            open_api_spec_file="/path/to/.settings/swagger_spec.yaml"
        )


if __name__ == "__main__":
    pytest.main()
