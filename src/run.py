from flask import Flask

import app.models
from app.api import configure_hooks, register_blueprint
from app.api.error_handlers import register_error_handler
from app.config import configure_app
from app.database import init_db

app = Flask(__name__)  # noqa
configure_app(app)
init_db(app)
register_blueprint(app)
register_error_handler(app)
configure_hooks(app)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
