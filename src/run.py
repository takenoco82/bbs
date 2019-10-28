from flask import Flask

from app.config import configure_app
from app.database import init_db
from app.api import register_blueprint
import app.models

app = Flask(__name__)  # noqa
configure_app(app)
init_db(app)
register_blueprint(app)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
