from marshmallow import Schema, fields
from dataclasses import dataclass, field
from typing import List


@dataclass
class ErrorInfo:
    code: str = None
    field: str = None
    description: str = None


@dataclass
class Errors:
    request_id: str = None
    status: str = None
    message: str = None
    errors: List[ErrorInfo] = field(default_factory=list)


class ErrorSchema(Schema):
    class Meta:
        fields = [field[0] for field in ErrorInfo.__dataclass_fields__.items()]


class ErrorsSchema(Schema):
    errors = fields.Nested(ErrorSchema, many=True, default=[])

    class Meta:
        fields = [field[0] for field in Errors.__dataclass_fields__.items()]
