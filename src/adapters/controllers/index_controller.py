from flask import Blueprint
from src.adapters.controllers.handlers.handler import handle_success


index = Blueprint("index", __name__, url_prefix="/")


@index.route("/", methods=["GET"])
def index_controller():
    return handle_success()
