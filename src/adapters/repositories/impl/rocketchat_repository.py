from src.entities.message_client import MergeRequestMessage
from src.adapters.repositories.message_client_repository import MessageClientRepository
from src.workers.impl.rocketchat import RocketchatWorker
import textwrap


class RocketchatRepository(MessageClientRepository):
    def post_group_chat_message(self, message: MergeRequestMessage) -> None:
        # Structure like [@user1, @user2]
        reviewers = ", ".join(
            ["@{reviewer}".format(reviewer=reviewer.username) for reviewer in message.reviewers]
        )

        merge_request_message = textwrap.dedent(
            """\
            <b>{title}</b>
            Merge Request created by @{user}
            Please review {reviewers}
            {request}""".format(
                title=message.title,
                user=message.author.username,
                reviewers=reviewers,
                request=message.url,
            )
        )

        RocketchatWorker.send_to_all_active_chats(merge_request_message)
