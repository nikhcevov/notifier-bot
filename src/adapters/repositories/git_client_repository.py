from abc import ABCMeta, abstractmethod
from src.entities.git_client import MergeRequest
from src.entities.message_client import MergeRequestCreatedMessage, MergeRequestApprovedMessage


class GitClientRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_merge_request_created_message(
        self, merge_request: MergeRequest
    ) -> MergeRequestCreatedMessage:
        raise NotImplementedError()

    @abstractmethod
    def get_merge_request_approved_message(
        self, merge_request: MergeRequest
    ) -> MergeRequestApprovedMessage:
        raise NotImplementedError()
