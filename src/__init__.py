import os
import uvicorn
from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from src.workers.telegram import worker_instance
from src.adapters.controllers.error_controller import errors
from src.adapters.controllers.gitlab_controller import gitlab
from src.adapters.controllers.index_controller import index


flask_config = {
    "production": "config.ProdConfig",
    "development": "config.DevConfig",
    "test": "config.TestConfig",
}


def create_flask_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(flask_config[os.environ.get("ENV", "development")])

    flask_app.register_blueprint(index)
    flask_app.register_blueprint(errors)
    flask_app.register_blueprint(gitlab)

    return flask_app


async def main() -> None:
    flask_app = create_flask_app()

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=WsgiToAsgi(flask_app),
            port=8080,
            use_colors=False,
            host="0.0.0.0",
        )
    )

    telegram_worker = await worker_instance.init_worker()

    # Run application and webserver together
    async with telegram_worker:
        await telegram_worker.start()
        await webserver.serve()
        await telegram_worker.stop()
