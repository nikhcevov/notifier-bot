import json
from flask import Blueprint, request
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.use_cases.gitlab.impl.merge_request_use_case import MergeRequestUseCase
from src.adapters.repositories.impl.gitlab_repository import GitlabRepository
from src.adapters.repositories.impl.telegram_repository import TelegramRepository
from src.adapters.controllers.handlers.handler import handle_success
from dacite import from_dict


gitlab = Blueprint("gitlab", __name__, url_prefix="/gitlab")


@gitlab.route("/webhook", methods=["POST"])
def gitlab_controller():
    data = json.loads(request.get_data())
    req = from_dict(data_class=MergeRequestRequest, data=data)

    git_client_repo = GitlabRepository()
    message_client_repo = TelegramRepository()

    MergeRequestUseCase(git_client_repo, message_client_repo).handle(req)

    return handle_success()
