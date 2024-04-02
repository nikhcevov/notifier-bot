import dataclasses
from typing import List


@dataclasses.dataclass
class User:
    id: int
    username: str


@dataclasses.dataclass
class ObjectAttributes:
    url: str
    title: str


@dataclasses.dataclass
class MergeRequest:
    object_kind: str
    reviewers: List[User]
    user: User
    object_attributes: ObjectAttributes
