from app.api.controllers import __all__ as blueprints
from app.api.hooks import (
    after_request_handlers,
    before_request_handlers,
    teardown_appcontext_handlers,
    teardown_request_handlers,
)


def register_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_hooks(app):
    app.before_request(before_request_handlers)
    app.after_request(after_request_handlers)
    app.teardown_request(teardown_request_handlers)
    app.teardown_appcontext(teardown_appcontext_handlers)
