from marshmallow import ValidationError

from app.api.controllers import __all__ as blueprints
from app.api.error_handlers import application_error_handler, validation_error_handler
from app.api.hooks import (
    after_request_handlers,
    before_request_handlers,
    teardown_appcontext_handlers,
    teardown_request_handlers,
)


def register_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def register_error_handler(app):
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(Exception, application_error_handler)


def configure_hooks(app):
    app.before_request(before_request_handlers)
    app.after_request(after_request_handlers)
    app.teardown_request(teardown_request_handlers)
    app.teardown_appcontext(teardown_appcontext_handlers)
