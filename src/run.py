from flask import Flask

from app.config import configure_app
from app.database import init_db
import app.models


app = Flask(__name__)  # noqa
configure_app(app)
init_db(app)


@app.route('/')
def hello():
    name = "Hello World\n"
    return name


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
