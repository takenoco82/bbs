from flask import Flask

from app.config import configure_app
from app.database import init_db
from app.api import register_blueprint, register_error_handler
import app.models

app = Flask(__name__)  # noqa
configure_app(app)
init_db(app)
register_blueprint(app)
register_error_handler(app)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
