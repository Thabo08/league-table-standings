import pytest

from main.main import get_input
from main.main import league_rankings
from main.main import match_result
from main.main import write_output


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


def test_correct_match_result_returned():
    team_1, team_2 = match_result("Team1 3, Team2 0")
    assert team_1.name == "Team1"
    assert team_2.name == "Team2"
    assert team_1.points == 3
    assert team_2.points == 0


def test_value_error_raise_when_no_teams_with_points_exist():
    with pytest.raises(ValueError):
        league_rankings({})


def test_correct_league_standings_returned():
    teams = {'Team3': 7, 'Team1': 0, 'Team4': 6, 'Team2': 1, 'Team5': 0}
    expected_standings = "1. Team3, 7 pts\n2. Team4, 6 pts\n" \
                         "3. Team2, 1 pt\n4. Team1, 0 pts\n4. Team5, 0 pts"
    actual_standings = league_rankings(teams)
    assert expected_standings == actual_standings


def test_value_error_raised_when_no_output_args_provided():
    with pytest.raises(ValueError):
        write_output(output="", to_file=None, to_stdout=None)


def test_contents_written_to_file():
    import os
    expected_standings = "1. Team3, 7 pts\n2. Team4, 6 pts\n" \
                         "3. Team2, 1 pt\n4. Team1, 0 pts\n4. Team5, 0 pts"
    write_output(expected_standings, to_file="sample_output.txt", to_stdout=None)
    with open("sample_output.txt") as f:
        file_contents = f.read()
    try:
        os.remove("sample_output.txt")
    except Exception:
        pass

    assert expected_standings == file_contents


def test_value_error_raised_when_no_input_args_provided():
    with pytest.raises(ValueError):
        get_input(from_file=None, from_stdin=None)
