import uuid
from datetime import datetime

from marshmallow import Schema, fields, post_load

from app.models import Thread


class ThreadSchema(Schema):
    id = fields.Str()
    title = fields.Str(required=True)
    created_at = fields.DateTime()

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
