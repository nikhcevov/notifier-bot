import os
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


TOKEN = os.environ["TELEGRAM_TOKEN"]


class TelegramWorker:
    def __init__(self):
        self.__active_chat_ids = {}
        self.__worker = None

    async def __start(self, update: Update, context: CallbackContext) -> None:
        """Display a message on start bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = update.message.chat_id

        if str(chat_id) in self.__active_chat_ids:
            await update.message.reply_html(text="This bot is already active in this chat.")
        else:
            await update.message.reply_html(text="Hello! \n\nThis bot is now active in this chat. ")
            self.__active_chat_ids[chat_id] = True

    async def __stop(self, update: Update, context: CallbackContext):
        """Display a message on stop bot command."""
        if update.message is None:
            logger.error("Update message is None")
            return

        chat_id = update.message.chat_id
        del self.__active_chat_ids[chat_id]

        await update.message.reply_html(
            text="Goodbye! \n\nThank you for using the Gitlab Integration Bot!"
        )

    async def __send_message_to_chat(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message to a chat."""
        job = context.job

        if job is None or job.chat_id is None or job.data is None:
            logger.error("Job is None or missing chat_id or data")
            return

        # check that job.data is a string
        if not isinstance(job.data, str):
            return

        await context.bot.send_message(job.chat_id, text=job.data, parse_mode=ParseMode.HTML)

    def send_to_all_active_chats(self, message: str) -> None:
        """Send a message to all active chats."""

        if self.__worker is None or self.__worker.job_queue is None:
            logger.error("Job queue is None")
            return

        for chat_id in self.__active_chat_ids:
            self.__worker.job_queue.run_once(
                callback=self.__send_message_to_chat, when=0, chat_id=chat_id, data=message
            )

    def init_worker(self) -> Application:
        logger.log(logging.INFO, "Starting Telegram Worker")

        self.__worker = Application.builder().token(TOKEN).build()
        self.__worker.add_handler(CommandHandler("start", self.__start))
        self.__worker.add_handler(CommandHandler("stop", self.__stop))

        return self.__worker


worker_instance = TelegramWorker()
