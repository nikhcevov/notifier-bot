import os
from flask import request
from src.entities.gitlab import MergeRequest
from src.adapters.repositories.gitlab_repository import GitlabRepository


class TelegramGitlabRepository(GitlabRepository):
    def merge_request(self, merge_request: MergeRequest) -> str:
        # Structure like [@user1, @user2]
        reviewers = ", ".join(
            [
                "@{reviewer}".format(reviewer=reviewer.username)
                for reviewer in merge_request.reviewers
            ]
        )

        merge_request_message = """
        Request {title}
        Merge Request created by @{user}
        Please review @{reviewers}
        {request}
        """.format(
            title=merge_request.object_attributes.title,
            user=merge_request.user.username,
            reviewers=reviewers,
            request=merge_request.object_attributes.url,
        )

        # TODO: Send message to Telegram

        return merge_request_message
