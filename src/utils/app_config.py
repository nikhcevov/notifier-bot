from src.utils.get_active_message_clients import get_active_message_clients


class AppConfig:
    message_clients = get_active_message_clients()
