from dataclasses import dataclass
from typing import List
from src.exception.errors import ValidationError
from src.entities.git_client import User, MergeRequestDetails


@dataclass
class MergeRequestRequest:
    object_kind: str
    reviewers: List[User]
    user: User
    object_attributes: MergeRequestDetails

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
