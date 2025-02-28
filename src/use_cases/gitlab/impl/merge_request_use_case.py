import logging
from src.adapters.repositories.git_client_repository import GitClientRepository
from src.adapters.repositories.message_client_repository import MessageClientRepository
from src.entities.git_client import MergeRequest, User
from src.exception.errors import UnexpectedError
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.use_cases.gitlab.merge_request_use_case import AbstractMergeRequestUseCase


class MergeRequestUseCase(AbstractMergeRequestUseCase):
    def __init__(
        self, git_client_repo: GitClientRepository, message_client_repo: MessageClientRepository
    ):
        self._git_client_repo = git_client_repo
        self._message_client_repo = message_client_repo

    async def handle(self, request: MergeRequestRequest) -> None:
        try:
            mr_entity = MergeRequest(
                id=str(request.object_attributes.id),
                event_name=request.object_kind,
                event_action=request.object_attributes.action,
                user=User(username=request.user.username, id=str(request.user.id)),
                url=request.object_attributes.url,
                title=request.object_attributes.title,
                reviewers=[
                    User(username=reviewer.username, id=str(reviewer.id))
                    for reviewer in request.reviewers
                ],
            )

            if request.object_attributes.action == "open":
                message = self._git_client_repo.get_merge_request_created_message(mr_entity)
                await self._message_client_repo.post_message(message)

            if request.object_attributes.action == "approved":
                message = self._git_client_repo.get_merge_request_approved_message(mr_entity)

                print(message, mr_entity.id)
                await self._message_client_repo.update_message(merge_request=message)

        except Exception as e:
            logging.exception(e)
            raise UnexpectedError("Failed to create merge request message.")
