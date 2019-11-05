from flask import Blueprint, jsonify, request

from app.api.schemas import ThreadSchema


bp = Blueprint("post_thread", __name__)


@bp.route("/threads", methods=["POST"])
def post_thread():
    requestBody = request.get_json()
    thread = ThreadSchema().load(requestBody)
    thread.save()

    responseBody = ThreadSchema().dump(thread)
    return (jsonify(responseBody), 201)
