from flask import Flask

import app.models
from app.api import register_blueprint
from app.api.error_handlers import register_error_handler
from app.api.hooks import configure_hooks
from app.config import init_app_config
from app.logging_config import init_logging_config
from app.open_api_spec import load_open_api_spec
from app.database import init_db

app = Flask(__name__)  # noqa
init_app_config(app)
init_logging_config(app)
load_open_api_spec(app)
init_db(app)
register_blueprint(app)
register_error_handler(app)
configure_hooks(app)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
