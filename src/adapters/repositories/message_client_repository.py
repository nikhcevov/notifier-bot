from abc import ABCMeta, abstractmethod
from src.entities.message_client import MergeRequestMessage


class MessageClientRepository(metaclass=ABCMeta):
    @abstractmethod
    def post_group_chat_message(self, message: MergeRequestMessage) -> None:
        raise NotImplementedError()
