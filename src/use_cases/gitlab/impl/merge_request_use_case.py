import logging

from src.adapters.repositories.gitlab_repository import GitlabRepository
from src.entities.gitlab import MergeRequest
from src.exception.errors import UnexpectedError
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.use_cases.gitlab.merge_request_use_case import AbstractMergeRequestUseCase


class MergeRequestUseCase(AbstractMergeRequestUseCase):
    def __init__(self, gitlab_repo: GitlabRepository):
        self._gitlab_repo = gitlab_repo

    def handle(self, request: MergeRequestRequest) -> None:
        try:
            self._gitlab_repo.merge_request(
                MergeRequest(
                    object_kind=request.object_kind,
                    reviewers=request.reviewers,
                    user=request.user,
                    object_attributes=request.object_attributes,
                )
            )
        except Exception as e:
            logging.exception(e)
            raise UnexpectedError("Failed to create merge request message.")
