import logging

from src.adapters.repositories.git_client_repository import GitClientRepository
from src.adapters.repositories.message_client_repository import MessageClientRepository
from src.entities.git_client import MergeRequest
from src.exception.errors import UnexpectedError
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.use_cases.gitlab.merge_request_use_case import AbstractMergeRequestUseCase


class MergeRequestUseCase(AbstractMergeRequestUseCase):
    def __init__(
        self, git_client_repo: GitClientRepository, message_client_repo: MessageClientRepository
    ):
        self._gitlab_repo = git_client_repo
        self._message_client_repo = message_client_repo

    def handle(self, request: MergeRequestRequest) -> None:
        try:
            message = self._gitlab_repo.get_merge_request_message(
                MergeRequest(
                    event_name=request.object_kind,
                    reviewers=request.reviewers,
                    user=request.user,
                    details=request.object_attributes,
                )
            )

            self._message_client_repo.post_group_chat_message(message)

        except Exception as e:
            logging.exception(e)
            raise UnexpectedError("Failed to create merge request message.")
