import uuid
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from app.api.schemas import ThreadSchema
from app.models import Thread


bp = Blueprint("post_thread", __name__)


@bp.route("/threads", methods=["POST"])
def post_thread():
    request_body = request.get_json()
    thread = _deserialize(request_body)

    Thread.save(thread)

    response_body = _serialize(thread)
    return (jsonify(response_body), 201)


def _deserialize(request_body):
    thread = ThreadSchema().load(request_body)

    utcnow = datetime.now(tz=timezone.utc)
    thread.id = str(uuid.uuid4())
    thread.created_at = utcnow
    thread.updated_at = utcnow
    return thread


def _serialize(model):
    return ThreadSchema().dump(model)
