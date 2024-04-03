from src.entities.git_client import MergeRequest
from src.entities.message_client import MergeRequestMessage, User
from src.adapters.repositories.git_client_repository import GitClientRepository


class GitlabRepository(GitClientRepository):
    def get_merge_request_message(self, merge_request: MergeRequest) -> MergeRequestMessage:
        return MergeRequestMessage(
            author=User(username=merge_request.user.username),
            title=merge_request.details.title,
            url=merge_request.details.url,
            reviewers=[User(username=reviewer.username) for reviewer in merge_request.reviewers],
        )
