from abc import ABCMeta, abstractmethod
from src.entities.git_client import MergeRequest
from src.entities.message_client import MergeRequestMessage


class GitClientRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_merge_request_message(self, merge_request: MergeRequest) -> MergeRequestMessage:
        raise NotImplementedError()
