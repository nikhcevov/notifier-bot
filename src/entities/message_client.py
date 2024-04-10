from typing import List

from dataclasses import dataclass


@dataclass
class User:
    username: str


@dataclass
class MergeRequestCreatedMessage:
    author: User
    reviewers: List[User]
    url: str
    title: str
    id: str
    action: str


@dataclass
class MergeRequestApprovedMessage:
    id: str
    approvedBy: User


@dataclass
class MergeRequestEntityChat:
    chat_id: str
    message_id: str


@dataclass
class MergeRequestEntity:
    id: str
    chats: List[MergeRequestEntityChat]
