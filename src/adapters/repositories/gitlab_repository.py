from abc import ABCMeta, abstractmethod
from src.entities.gitlab import MergeRequest


class GitlabRepository(metaclass=ABCMeta):
    @abstractmethod
    def merge_request(self, merge_request: MergeRequest) -> None:
        raise NotImplementedError()
