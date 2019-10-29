from flask import Blueprint, jsonify

from app.api.schemas import ThreadSchema
from app.models import Thread


bp = Blueprint("get_threads", __name__)


@bp.route("/threads", methods=["GET"])
def get_threads():
    threads = Thread.find_list()
    return jsonify({"threads": ThreadSchema(many=True).dump(threads)}), 200
