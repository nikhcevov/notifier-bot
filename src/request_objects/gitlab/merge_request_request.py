from dataclasses import dataclass
from typing import List
from src.exception.errors import ValidationError


@dataclass
class User:
    username: str
    id: int

@dataclass
class MergeObjectAttributes:
    action: str
    id: int
    title: str
    url: str


@dataclass
class MergeRequestRequest:
    object_kind: str
    reviewers: List[User]
    user: User
    object_attributes: MergeObjectAttributes

    def __post_init__(self):
        if not self.object_kind:
            raise ValidationError("object_kind is required.")
        if not self.object_kind == "merge_request":
            raise ValidationError("object_kind must be merge_request.")
        if not self.reviewers:
            raise ValidationError("reviewers is required.")
        if not self.user:
            raise ValidationError("user is required.")
        if not self.object_attributes:
            raise ValidationError("object_attributes is required.")
