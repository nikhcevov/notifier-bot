import os
import logging
from src.workers.worker import Worker
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from typing import Optional

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


SERVER = os.environ["ROCKETCHAT_SERVER"]
CHANNELS = os.environ["ROCKETCHAT_CHANNELS"].split(",")


class RocketchatWorker(Worker):
    __app: Optional[RocketChat] = None

    @staticmethod
    def send_to_all_active_chats(message: str) -> None:
        """Send a message to all active chats."""

        if RocketchatWorker.__app is not None:
            for channel in CHANNELS:
                RocketchatWorker.__app.chat_post_message(message, channel=channel)

    @staticmethod
    async def start():
        logger.log(logging.INFO, "Starting Rocketchat Worker")

        with sessions.Session() as session:
            rocket = RocketChat("user", "pass", server_url=SERVER, session=session)
            RocketchatWorker.__app = rocket
