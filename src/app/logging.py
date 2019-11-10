import logging
import logging.config
from pathlib import Path

import yaml


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


def get_logging_config_file(app):
    return f"{app.root_path}/logging.yaml"


def configure_logging(app):
    logging_config_file = get_logging_config_file(app)
    logging_config = Logging(logging_config_file).config

    logging.config.dictConfig(logging_config)

    # FlaskのLoggerを無効化する
    app.logger.disabled = True
    # werkzeugのLoggerを無効化する
    logging.getLogger("werkzeug").disabled = True
