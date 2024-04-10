from abc import ABCMeta, abstractmethod
from typing import Coroutine, Any, List
from src.entities.message_client import MergeRequestEntityChat
from dataclasses import dataclass


@dataclass
class PostedMessage:
    chat_id: str
    message_id: str


class Worker(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    async def start() -> Coroutine[Any, Any, None]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def post_message(message: str) -> List[PostedMessage]:
        """Send a message to all active chats and return the list of chats that the message was sent to."""
        raise NotImplementedError()
