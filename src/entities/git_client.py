from typing import List
from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str


@dataclass
class MergeRequest:
    id: str
    event_name: str
    event_action: str
    reviewers: List[User]
    user: User
    url: str
    title: str
