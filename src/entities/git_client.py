from typing import List
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str


@dataclass
class MergeRequestDetails:
    url: str
    title: str


@dataclass
class MergeRequest:
    event_name: str
    reviewers: List[User]
    user: User
    details: MergeRequestDetails
