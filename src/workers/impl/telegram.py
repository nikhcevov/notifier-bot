import os
import logging
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ExtBot,
    JobQueue,
)
from src.workers.worker import Worker
from typing import Optional, Dict, Any, List
from src.entities.message_client import MergeRequestEntityChat
from src.workers.worker import PostedMessage

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


TOKEN = os.environ["TELEGRAM_TOKEN"]


class TelegramWorker(Worker):
    __active_chat_ids: Dict[str, bool] = {}

    # TODO: How to type this as Application...build() return type?
    __app: Optional[
        Application[
            ExtBot[None],
            Any,
            Dict[Any, Any],
            Dict[Any, Any],
            Dict[Any, Any],
            JobQueue[Any],
        ]
    ] = None

    @staticmethod
    async def __start(update: Update, context: CallbackContext) -> None:
        logger.info("Start command received")

        """Display a message on start bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = str(update.message.chat_id)

        if str(chat_id) in TelegramWorker.__active_chat_ids:
            await update.message.reply_html(text="This bot is already active in this chat.")
        else:
            await update.message.reply_html(text="Hello! \n\nThis bot is now active in this chat. ")
            TelegramWorker.__active_chat_ids[chat_id] = True

    @staticmethod
    async def __stop(update: Update, context: CallbackContext):
        logger.info("Stop command received")

        """Display a message on stop bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = str(update.message.chat_id)
        del TelegramWorker.__active_chat_ids[chat_id]

        await update.message.reply_html(
            text="Goodbye! \n\nThank you for using the Gitlab Integration Bot!"
        )

    @staticmethod
    async def post_message(message: str) -> List[PostedMessage]:
        """Send a message to all active chats."""

        if TelegramWorker.__app is None:
            logger.error("Telegram app is not initialized")
            return []

        resp = []

        for chat_id in TelegramWorker.__active_chat_ids:
            # TODO: Run request in parallel
            chat_resp = await TelegramWorker.__app.bot.send_message(
                chat_id=chat_id, text=message, parse_mode=ParseMode.HTML
            )

            message_id = str(chat_resp["message_id"])
            resp.append(PostedMessage(chat_id=chat_id, message_id=message_id))

        return resp

    @staticmethod
    async def reply_to_message_id(message_id: str, chat_id: str, message: str) -> None:
        """Send a message to all active chats."""

        if TelegramWorker.__app is None:
            logger.error("Telegram app is not initialized")
            return

        await TelegramWorker.__app.bot.send_message(
            chat_id=int(chat_id),
            text=message,
            parse_mode=ParseMode.HTML,
            reply_to_message_id=int(message_id),
        )

    @staticmethod
    async def start():
        logger.log(logging.INFO, "Starting Telegram Worker")

        TelegramWorker.__app = Application.builder().token(TOKEN).build()
        TelegramWorker.__app.add_handler(CommandHandler("start", TelegramWorker.__start))
        TelegramWorker.__app.add_handler(CommandHandler("stop", TelegramWorker.__stop))

        await TelegramWorker.__app.initialize()

        if TelegramWorker.__app.updater is not None:
            logger.log(logging.INFO, "Start polling")
            await TelegramWorker.__app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        await TelegramWorker.__app.start()
