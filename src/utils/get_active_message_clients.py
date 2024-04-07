import os

from typing import Literal, List


def get_active_message_clients() -> List[Literal["TELEGRAM", "ROCKETCHAT"]]:
    is_telegram_worker_active = os.environ.get("TELEGRAM_ENABLED", "false") == "true"
    is_rocketchat_worker_active = os.environ.get("ROCKETCHAT_ENABLED", "false") == "true"

    clients = []

    if is_telegram_worker_active:
        clients.append("TELEGRAM")

    if is_rocketchat_worker_active:
        clients.append("ROCKETCHAT")

    return clients
