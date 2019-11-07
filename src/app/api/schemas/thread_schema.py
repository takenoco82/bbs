import uuid
from datetime import datetime

from marshmallow import Schema, fields, post_load, validate

from app.models import Thread


class ThreadSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.Length(min=1, max=128)
    )
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def to_model(self, data, **kwargs):
        utcnow = datetime.utcnow()
        default_params = {
            "id": str(uuid.uuid4()),
            "created_at": utcnow,
            "updated_at": utcnow,
        }
        params = {**default_params, **data}
        return Thread(**params)
