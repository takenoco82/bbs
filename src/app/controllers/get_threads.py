from flask import Blueprint, jsonify

from app.models import Thread
from app.schemas import ThreadSchema


bp = Blueprint("get_threads", __name__)


@bp.route("/threads", methods=["GET"])
def get_threads():
    threads = Thread.query.order_by(Thread.updated_at.asc()).all()
    return jsonify({"threads": ThreadSchema(many=True).dump(threads)}), 200
