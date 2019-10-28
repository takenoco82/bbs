import pytest
from app.config import Config


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
class TestConfigMode:
    from app.config import ProductionConfig, DevelopmentConfig, TestConfig

    @pytest.mark.parametrize(
        "input, expected",
        [
            (None, ProductionConfig),
            ("production", ProductionConfig),
            ("development", DevelopmentConfig),
            ("test", TestConfig),
        ]
    )
    def test_get_config_object(self, monkeypatch, input, expected):
        from app.config import get_config_object

        if input:
            monkeypatch.setenv("BBS_APP_CONFIG", input)
            config_obj = get_config_object()
            assert isinstance(config_obj, expected)
        else:
            monkeypatch.delenv("BBS_APP_CONFIG", raising=False)
            config_obj = get_config_object()
            assert isinstance(config_obj, expected)


if __name__ == "__main__":
    pytest.main()
