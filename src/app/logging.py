import logging
import logging.config
from pathlib import Path

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


class Logging:
    def __init__(self, logging_config_file=None):
        self.logging_config_file = logging_config_file

    @property
    def config(self):
        basic_config = {"version": 1, "disable_existing_loggers": False}

        custom_config = {}
        if self.logging_config_file and Path(self.logging_config_file).exists():
            with open(self.logging_config_file, "r") as f:
                custom_config = yaml.load(f, Loader=yaml.SafeLoader)

        return {**basic_config, **custom_config}


def configure_logging(app, logging_config_file=None):
    logging_config = Logging(logging_config_file).config

    logging.config.dictConfig(logging_config)

    # FlaskのLoggerを無効化する
    app.logger.disabled = True
    # werkzeugのLoggerを無効化する
    logging.getLogger("werkzeug").disabled = True
