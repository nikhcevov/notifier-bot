from src.adapters.repositories.git_client_repository import GitClientRepository
from src.entities.git_client import MergeRequest
from src.entities.message_client import (
    MergeRequestCreatedMessage,
    MergeRequestApprovedMessage,
    User,
)


class GitlabRepository(GitClientRepository):
    def get_merge_request_created_message(
        self, merge_request: MergeRequest
    ) -> MergeRequestCreatedMessage:
        return MergeRequestCreatedMessage(
            author=User(username=merge_request.user.username),
            title=merge_request.title,
            url=merge_request.url,
            id=str(merge_request.id),
            action=merge_request.event_action,
            reviewers=[User(username=reviewer.username) for reviewer in merge_request.reviewers],
        )

    def get_merge_request_approved_message(
        self, merge_request: MergeRequest
    ) -> MergeRequestApprovedMessage:
        return MergeRequestApprovedMessage(
            approvedBy=User(username=merge_request.user.username),
            id=str(merge_request.id),
        )
