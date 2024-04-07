import os
import uvicorn
from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from src.adapters.controllers.error_controller import errors
from src.adapters.controllers.gitlab_controller import gitlab
from src.adapters.controllers.index_controller import index
import asyncio
from typing import List
from src.workers.worker import Worker
from src.workers.impl.telegram import TelegramWorker
from src.utils.app_config import AppConfig

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


async def init_workers() -> List[Worker]:
    workers = []

    if AppConfig.message_clients.count("TELEGRAM") > 0:
        workers.append(TelegramWorker)

    if AppConfig.message_clients.count("ROCKETCHAT") > 0:
        # workers.append()
        pass

    return workers


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

    workers = await init_workers()

    # Run workers and webserver concurrently
    await asyncio.gather(webserver.serve(), *(worker.start() for worker in workers))
