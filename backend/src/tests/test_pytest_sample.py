import pytest


@pytest.mark.small
class TestPytestBasic:
    def test_ok(self):
        pass

    def test_string_ok(self):
        assert "aha" == "aha"

    @pytest.mark.skip(reason="NG")
    def test_string_ng(self):
        assert "aha" == "ihi"

    def test_int_ok(self):
        assert 42 == 42

    @pytest.mark.skip(reason="NG")
    def test_int_ng(self):
        assert 42 == 0

    def test_float_ok(self):
        assert 3.14 == 3.14

    @pytest.mark.skip(reason="NG")
    def test_float_ng(self):
        assert 3.14 == 3.141519

    def test_dict_ok(self):
        assert {"key": "aha", "value": 1} == {"key": "aha", "value": 1}

    @pytest.mark.skip(reason="NG")
    def test_dict_ng(self):
        assert {"key": "aha", "value": 1} == {"key": "ihi", "value": 2}

    def test_list_ok(self):
        assert [2, 1, 3] == [2, 1, 3]

    @pytest.mark.skip(reason="NG")
    def test_list_ng(self):
        assert [2, 1, 3] == [2, 3]

    def test_dict_list_ok(self):
        actual = [{"value": 1}, {"value": 3}, {"value": 2}]
        expected = [{"value": 1}, {"value": 3}, {"value": 2}]
        assert actual == expected

    @pytest.mark.skip(reason="NG")
    def test_dict_list_ng(self):
        actual = [{"value": 1}, {"value": 3}, {"value": 2}]
        expected = [{"value": 3}, {"aha": 3}, {"value": 2}]
        assert actual == expected


@pytest.mark.small
class TestPytestParametrize:
    """Parametrizing tests — pytest documentation

    http://doc.pytest.org/en/latest/example/parametrize.html
    """

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            ("3+5", 8),
            # ("6*9", 42),
            ("2+4", 6),
        ],
    )
    def test_eval(self, test_input, expected):
        assert eval(test_input) == expected


@pytest.mark.small
class TestPytestFixture:
    """Monkeypatching/mocking modules and environments — pytest documentation

    https://docs.pytest.org/en/latest/monkeypatch.html
    """

    def get_os_user_lower(self):
        """Simple retrieval function.
        Returns lowercase USER or raises EnvironmentError."""

        import os

        username = os.getenv("USER")

        if username is None:
            raise OSError("USER environment is not set.")

        return username.lower()

    @pytest.fixture
    def mock_env_user(self, monkeypatch):
        monkeypatch.setenv("USER", "TestingUser")

    @pytest.fixture
    def mock_env_missing(self, monkeypatch):
        monkeypatch.delenv("USER", raising=False)

    # notice the tests reference the fixtures for mocks
    def test_upper_to_lower(self, mock_env_user):
        assert self.get_os_user_lower() == "testinguser"

    def test_raise_exception(self, mock_env_missing):
        with pytest.raises(OSError):
            _ = self.get_os_user_lower()


if __name__ == "__main__":
    import pytest

    pytest.main()
