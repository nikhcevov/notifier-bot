from abc import ABCMeta, abstractmethod

from src.request_objects.gitlab.merge_request_request import MergeRequestRequest


class AbstractMergeRequestUseCase(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, request: MergeRequestRequest) -> None:
        raise NotImplementedError()
