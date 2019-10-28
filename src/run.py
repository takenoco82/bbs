from flask import Flask

from app.config import configure_app
from app.controllers import __all__ as apis
from app.database import init_db
import app.models

app = Flask(__name__)  # noqa
configure_app(app)
init_db(app)

# Blueprintの登録
for api in apis:
    app.register_blueprint(api)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
