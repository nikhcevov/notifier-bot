import json
import os
from flask import Blueprint, request
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.request_objects.gitlab.webhook_request import WebhookRequest
from src.use_cases.gitlab.impl.merge_request_use_case import MergeRequestUseCase
from src.adapters.repositories.gitlab_repository import GitlabRepository
from src.adapters.repositories.impl.telegram_gitlab_repository import TelegramGitlabRepository
from src.adapters.controllers.handlers.handler import handle_success, handle_validation_error


repos: list[GitlabRepository] = []
telegram_enabled = os.environ["TELEGRAM_ENABLED"] == "true"
rocketchat_enabled = os.environ["ROCKETCHAT_ENABLED"] == "true"

if telegram_enabled:
    repos.append(TelegramGitlabRepository())
# TODO: Add RocketChat repository
if rocketchat_enabled:
    pass


gitlab = Blueprint("gitlab", __name__, url_prefix="/gitlab")


@gitlab.route("/webhook", methods=["POST"])
def gitlab_controller():
    data = json.loads(request.get_data())
    hook_req = WebhookRequest(**data)

    if hook_req.object_kind == "merge_request":
        req = MergeRequestRequest(**data)

        for repo in repos:
            MergeRequestUseCase(repo).handle(req)

        return handle_success()

    return handle_validation_error("Invalid request object kind.")
