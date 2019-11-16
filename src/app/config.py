import os

from werkzeug.utils import import_string

from app.logging_config import configure_logging
from app.open_api_spec import load_open_api_spec


config_mode = {
    "production": "app.config.ProductionConfig",
    "development": "app.config.DevelopmentConfig",
    "test": "app.config.TestingConfig",
}


class Config:
    # SQLAlchemy
    #   https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        MYSQL_USER = os.getenv("MYSQL_USER", "admin")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "admin")
        MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
        MYSQL_PORT = "3306"
        MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "bbs")
        MYSQL_CHARSET = "utf8mb4"

        return (
            f"mysql+pymysql://"
            f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
            f"?charset={MYSQL_CHARSET}"
        )

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    # Flask
    TESTING = True


class TestingConfig(Config):
    # Flask
    TESTING = True


def get_config_object():
    config_name = os.getenv("BBS_APP_CONFIG", "production")
    return import_string(config_mode[config_name])()


def init_app_config(app):
    config_object = get_config_object()
    app.config.from_object(config_object)

    configure_logging(
        app, logging_config_file=f"{app.root_path}/.settings/logging.yaml"
    )
    load_open_api_spec(
        open_api_spec_file=f"{app.root_path}/.settings/swagger_spec.yaml"
    )
