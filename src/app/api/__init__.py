from marshmallow import ValidationError

from app.api.controllers import __all__ as blueprints
from app.api.error_handlers import validation_error_handler


def register_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def register_error_handler(app):
    app.register_error_handler(ValidationError, validation_error_handler)
