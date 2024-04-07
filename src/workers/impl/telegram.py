import os
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler, ContextTypes
from src.workers.worker import Worker
from typing import Optional


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


TOKEN = os.environ["TELEGRAM_TOKEN"]


class TelegramWorker(Worker):
    __active_chat_ids = {}
    __app: Optional[Application] = None

    @staticmethod
    async def __start(update: Update, context: CallbackContext) -> None:
        logger.info("Start command received")

        """Display a message on start bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = update.message.chat_id

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

        chat_id = update.message.chat_id
        del TelegramWorker.__active_chat_ids[chat_id]

        await update.message.reply_html(
            text="Goodbye! \n\nThank you for using the Gitlab Integration Bot!"
        )

    @staticmethod
    async def __send_message_to_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message to a chat."""
        job = context.job

        if job is None or job.chat_id is None or job.data is None:
            logger.error("Job is None or missing chat_id or data")
            return

        if not isinstance(job.data, str):
            return

        await context.bot.send_message(job.chat_id, text=job.data, parse_mode=ParseMode.HTML)

    @staticmethod
    def send_to_all_active_chats(message: str) -> None:
        """Send a message to all active chats."""

        if TelegramWorker.__app is None or TelegramWorker.__app.job_queue is None:
            logger.error("Job queue is None")
            return

        for chat_id in TelegramWorker.__active_chat_ids:
            TelegramWorker.__app.job_queue.run_once(
                callback=TelegramWorker.__send_message_to_chat,
                when=0,
                chat_id=chat_id,
                data=message,
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
