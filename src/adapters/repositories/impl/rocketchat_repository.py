from src.entities.message_client import MergeRequestCreatedMessage
from src.adapters.repositories.message_client_repository import MessageClientRepository
from src.workers.impl.rocketchat import RocketchatWorker
import textwrap


class RocketchatRepository(MessageClientRepository):
    async def post_message(self, message: MergeRequestCreatedMessage) -> None:
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

        RocketchatWorker.post_message(merge_request_message)
