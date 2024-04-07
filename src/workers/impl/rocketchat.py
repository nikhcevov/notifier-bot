import os
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler, ContextTypes, MessageHandler
from src.workers.worker import Worker


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


TOKEN = os.environ["TELEGRAM_TOKEN"]


class RocketchatWorker(Worker):
    __active_chat_ids = {}
    __app = None

    @staticmethod
    async def __start(update: Update, context: CallbackContext) -> None:
        logger.info("Start command received")

        """Display a message on start bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = update.message.chat_id

        if str(chat_id) in RocketchatWorker.__active_chat_ids:
            await update.message.reply_html(text="This bot is already active in this chat.")
        else:
            await update.message.reply_html(text="Hello! \n\nThis bot is now active in this chat. ")
            RocketchatWorker.__active_chat_ids[chat_id] = True

    @staticmethod
    async def __stop(update: Update, context: CallbackContext):
        logger.info("Stop command received")

        """Display a message on stop bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = update.message.chat_id
        del RocketchatWorker.__active_chat_ids[chat_id]

        await update.message.reply_html(
            text="Goodbye! \n\nThank you for using the Gitlab Integration Bot!"
        )

    @staticmethod
    async def __send_message_to_chat(TelegramWorker, context: ContextTypes.DEFAULT_TYPE) -> None:
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

        if RocketchatWorker.__app is None or RocketchatWorker.__app.job_queue is None:
            logger.error("Job queue is None")
            return

        for chat_id in RocketchatWorker.__active_chat_ids:
            RocketchatWorker.__app.job_queue.run_once(
                callback=RocketchatWorker.__send_message_to_chat,
                when=0,
                chat_id=chat_id,
                data=message,
            )

    @staticmethod
    async def init_worker() -> Application:
        logger.log(logging.INFO, "Starting Telegram Worker")

        RocketchatWorker.__app = Application.builder().token(TOKEN).build()
        RocketchatWorker.__app.add_handler(CommandHandler("start", RocketchatWorker.__start))
        RocketchatWorker.__app.add_handler(CommandHandler("stop", RocketchatWorker.__stop))

        await RocketchatWorker.__app.initialize()

        if RocketchatWorker.__app.updater is not None:
            logger.log(logging.INFO, "Start polling")
            await RocketchatWorker.__app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        return RocketchatWorker.__app

    @staticmethod
    async def start():
        if RocketchatWorker.__app is not None:
            return RocketchatWorker.__app.start()
