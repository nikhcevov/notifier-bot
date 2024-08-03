import os
import logging
from src.workers.worker import Worker
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from typing import Optional
from requests import Response

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


SERVER = os.environ["ROCKETCHAT_SERVER"]
CHANNELS = os.environ["ROCKETCHAT_CHANNELS"].split(",")
USER = os.environ["ROCKETCHAT_USER"]
PASS = os.environ["ROCKETCHAT_PASSWORD"]


class RocketchatWorker(Worker):
    __app: Optional[RocketChat] = None

    @staticmethod
    def post_message(message: str) -> None:
        """Send a message to all active chats."""

        if RocketchatWorker.__app is not None:
            for channel in CHANNELS:
                resp = RocketchatWorker.__app.chat_post_message(message, channel=channel)
                print(resp)

    @staticmethod
    async def start():
        logger.log(logging.INFO, "Starting Rocketchat Worker")

        with sessions.Session() as session:
            rocket = RocketChat(USER, PASS, server_url=SERVER, session=session)
            RocketchatWorker.__app = rocket
            print(rocket.me().json())
