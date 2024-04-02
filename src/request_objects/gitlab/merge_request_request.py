import dataclasses
from typing import List
from src.exception.errors import ValidationError
from src.entities.gitlab import User, ObjectAttributes


@dataclasses.dataclass
class MergeRequestRequest:
    object_kind: str
    reviewers: List[User]
    user: User
    object_attributes: ObjectAttributes

    def __post_init__(self):
        if not self.object_kind:
            raise ValidationError("object_kind id is required.")
        if not self.object_kind == "merge_request":
            raise ValidationError("object_kind must be merge_request.")
        if not self.reviewers:
            raise ValidationError("reviewers id is required.")
        if not self.user:
            raise ValidationError("user id is required.")
        if not self.object_attributes:
            raise ValidationError("object_attributes id is required.")
