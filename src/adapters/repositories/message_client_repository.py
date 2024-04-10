from abc import ABCMeta, abstractmethod
from src.entities.message_client import MergeRequestCreatedMessage, MergeRequestApprovedMessage


class MessageClientRepository(metaclass=ABCMeta):
    @abstractmethod
    async def post_message(self, merge_request: MergeRequestCreatedMessage) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_message(self, merge_request: MergeRequestApprovedMessage) -> None:
        raise NotImplementedError()
