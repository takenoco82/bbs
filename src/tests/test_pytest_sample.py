import pytest


@pytest.mark.small
class TestPytestSample:
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

    # [Parametrizing tests — pytest documentation](http://doc.pytest.org/en/latest/example/parametrize.html)  # noqa
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


if __name__ == "__main__":
    import pytest

    pytest.main()
