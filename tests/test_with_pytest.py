import pytest

from main.main import match_result


def test_exception_raised_when_input_is_none():
    with pytest.raises(ValueError):
        match_result(None)


def test_value_error_raised_when_input_is_empty():
    with pytest.raises(ValueError):
        match_result("")


def test_value_error_raised_when_input_format_is_invalid():
    with pytest.raises(ValueError):
        match_result("Team1 3")


def test_value_error_raised_when_input_format_is_invalid_for_individual_team_result():
    with pytest.raises(ValueError):
        match_result("Team1 3, Team2")
