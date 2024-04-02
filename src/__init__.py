from flask import Flask
from os import getenv
from src.adapters.controllers.error_controller import errors
from src.adapters.controllers.gitlab_controller import gitlab
from src.adapters.controllers.index_controller import index


config = {
    "production": "config.ProdConfig",
    "development": "config.DevConfig",
    "test": "config.TestConfig",
}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[getenv("ENV", "development")])

    app.register_blueprint(index)
    app.register_blueprint(errors)
    app.register_blueprint(gitlab)

    return app
