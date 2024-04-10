import json
from flask import Blueprint, request
from dacite import from_dict
from src.request_objects.gitlab.merge_request_request import MergeRequestRequest
from src.use_cases.gitlab.impl.merge_request_use_case import MergeRequestUseCase
from src.adapters.repositories.impl.gitlab_repository import GitlabRepository
from src.adapters.repositories.impl.telegram_repository import TelegramRepository
from src.adapters.repositories.impl.rocketchat_repository import RocketchatRepository
from src.adapters.controllers.handlers.handler import handle_success
from src.utils.app_config import AppConfig

gitlab = Blueprint("gitlab", __name__, url_prefix="/gitlab")


def get_message_client_repos():
    message_client_repos = []

    if AppConfig.message_clients.count("TELEGRAM") > 0:
        message_client_repos.append(TelegramRepository())
    if AppConfig.message_clients.count("ROCKETCHAT") > 0:
        message_client_repos.append(RocketchatRepository())
        
    return message_client_repos


@gitlab.route("/webhook", methods=["POST"])
async def gitlab_controller():
    data = json.loads(request.get_data())

    req = from_dict(data_class=MergeRequestRequest, data=data)

    git_client_repo = GitlabRepository()

    message_client_repos = get_message_client_repos()

    for message_client_repo in message_client_repos:
        await MergeRequestUseCase(git_client_repo, message_client_repo).handle(req)

    return handle_success()
