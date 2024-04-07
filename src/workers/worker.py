from abc import ABCMeta, abstractmethod
from typing import Coroutine, Any


class Worker(metaclass=ABCMeta):
    @abstractmethod
    # @staticmethod
    async def start() -> Coroutine[Any, Any, None]:
        raise NotImplementedError()
