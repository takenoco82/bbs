from marshmallow import Schema


class ThreadSchema(Schema):
    class Meta:
        fields = ("id", "title", "created_at")
