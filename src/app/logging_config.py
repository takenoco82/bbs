import logging
import logging.config

import yaml
from flask import g


class RequestContextFilter(logging.Filter):
    """ログにリクエストコンテキストを付与するFilter

    See:
        https://docs.python.org/ja/3/howto/logging-cookbook.html#filters-contextual
        https://docs.python.org/ja/3/howto/logging-cookbook.html#configuring-filters-with-dictconfig
    """

    def filter(self, record):

        record.request_id = g.request_id
        return True


class LoggingConfig(dict):
    def __init__(self):
        dict.__init__(self, {"version": 1, "disable_existing_loggers": False})

    def update_from_yaml(self, path):
        with open(path, "r") as f:
            custom_config = yaml.load(f, Loader=yaml.SafeLoader)

        for key, value in custom_config.items():
            self[key] = value


def init_logging_config(app):
    logging_config = LoggingConfig()
    logging_config.update_from_yaml(f"{app.root_path}/.settings/logging.yaml")

    logging.config.dictConfig(logging_config)

    # FlaskのLoggerを無効化する
    app.logger.disabled = True
    # werkzeugのLoggerを無効化する
    logging.getLogger("werkzeug").disabled = True
