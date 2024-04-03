from typing import List

from dataclasses import dataclass


@dataclass
class User:
    username: str


@dataclass
class MergeRequestMessage:
    author: User
    reviewers: List[User]
    url: str
    title: str
