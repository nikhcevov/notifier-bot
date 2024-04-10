from src.entities.message_client import (
    MergeRequestCreatedMessage,
    MergeRequestEntity,
    MergeRequestEntityChat,
    MergeRequestApprovedMessage,
)
from src.adapters.repositories.message_client_repository import MessageClientRepository
from src.workers.impl.telegram import TelegramWorker
import textwrap
from dacite import from_dict

# aka database interface
# TODO: Use a real database
database = {}


class TelegramRepository(MessageClientRepository):
    async def post_message(self, merge_request: MergeRequestCreatedMessage) -> None:
        # Structure like [@user1, @user2]
        reviewers = ", ".join(
            [
                "@{reviewer}".format(reviewer=reviewer.username)
                for reviewer in merge_request.reviewers
            ]
        )

        merge_request_message = textwrap.dedent(
            """\
            <b>{title}</b>
            Merge Request created by @{user}
            Please review {reviewers}
            {request}""".format(
                title=merge_request.title,
                user=merge_request.author.username,
                reviewers=reviewers,
                request=merge_request.url,
            )
        )

        chats_resp = await TelegramWorker.post_message(merge_request_message)

        chats = [{"chat_id": chat.chat_id, "message_id": chat.message_id} for chat in chats_resp]

        database.update({merge_request.id: chats})
        print(database)

    async def update_message(self, merge_request: MergeRequestApprovedMessage) -> None:
        approved_message = "Approved by @" + merge_request.approvedBy.username

        for item in database[merge_request.id]:
            chat_id = item["chat_id"]
            message_id = item["message_id"]

            # TODO: Parallel
            await TelegramWorker.reply_to_message_id(
                message=approved_message, chat_id=chat_id, message_id=message_id
            )
