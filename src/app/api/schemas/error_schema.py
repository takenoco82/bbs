from marshmallow import Schema, fields


class ErrorSchema(Schema):
    code = fields.Str()
    field = fields.Str()
    message = fields.Str()
