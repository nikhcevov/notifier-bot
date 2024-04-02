import dataclasses
from src.exception.errors import ValidationError


@dataclasses.dataclass
class WebhookRequest:
    object_kind: str

    def __post_init__(self):
        if not self.object_kind:
            raise ValidationError("object_kind id is required.")
