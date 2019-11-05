from datetime import datetime
from unittest.mock import patch
from uuid import UUID

import pytest
from freezegun import freeze_time
from marshmallow import ValidationError

from app.api.schemas import ThreadSchema
from app.models import Thread


@pytest.mark.small
class TestThreadSchema:
    @patch("uuid.uuid4", return_value=UUID("add96e80-fb11-11e9-bc1d-0242ac170003"))
    @freeze_time("2019-01-02 12:34:56.123456")
    def test_load_normal(self, patcher):
        schema = ThreadSchema()
        actual = schema.load({"title": "title1"})
        expected = Thread(
            **{
                "id": "add96e80-fb11-11e9-bc1d-0242ac170003",
                "title": "title1",
                "created_at": datetime(2019, 1, 2, 12, 34, 56, 123456),
                "updated_at": datetime(2019, 1, 2, 12, 34, 56, 123456),
            }
        )
        assert patcher.called
        assert actual.__repr__() == expected.__repr__()

    def test_load_exception(self):
        schema = ThreadSchema()
        with pytest.raises(ValidationError):
            schema.load({})
