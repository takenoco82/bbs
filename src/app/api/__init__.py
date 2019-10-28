from app.api.controllers import __all__ as blueprints


def register_blueprint(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
