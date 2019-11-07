from marshmallow import Schema, fields, post_load, validate

from app.models import Thread


class ThreadSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(
        required=True, allow_none=False, validate=validate.Length(min=1, max=128)
    )
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def to_model(self, data, **kwargs):
        return Thread(**data)
