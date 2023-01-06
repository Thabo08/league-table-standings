from unittest import TestCase

import pytest

from main.main import RankManager
from main.main import get_input
from main.main import league_rankings
from main.main import match_points
from main.main import teams_with_points
from main.main import write_output


class TestRankManager(TestCase):
    def test_rank_manager_returns_correct_successive_ranks(self):
        rank_manager = RankManager()
        for i in range(1, 4):
            assert i == rank_manager.get_rank()

    def test_rank_manager_returns_same_rank(self):
        rank_manager = RankManager()
        rank_1 = rank_manager.get_rank()
        rank_2 = rank_manager.get_rank(same_points=True)
        rank_3 = rank_manager.get_rank(same_points=True)

        assert rank_1 == rank_2 == rank_3

    def test_rank_manager_returns_different_ranks(self):
        rank_manager = RankManager()
        rank_1 = rank_manager.get_rank()
        rank_2 = rank_manager.get_rank()
        rank_3 = rank_manager.get_rank()
        rank_4 = rank_manager.get_rank(same_points=True)
        rank_5 = rank_manager.get_rank()

        assert rank_1 == 1
        assert rank_2 == 2
        assert rank_3 == 3
        assert rank_4 == 3
        assert rank_5 == 5


def test_exception_raised_when_input_is_none():
    with pytest.raises(ValueError):
        match_points(None)


def test_value_error_raised_when_input_is_empty():
    with pytest.raises(ValueError):
        match_points("")


def test_value_error_raised_when_input_format_is_invalid():
    with pytest.raises(ValueError):
        match_points("Team1 3")


def test_value_error_raised_when_input_format_is_invalid_for_individual_team_result():
    with pytest.raises(ValueError):
        match_points("Team1 3, Team2")


def test_correct_match_result_returned():
    team_1, team_2 = match_points("Team1 3, Team2 0")
    assert team_1.name == "Team1"
    assert team_2.name == "Team2"
    assert team_1.points == 3
    assert team_2.points == 0


def test_value_error_raise_when_no_teams_with_points_exist():
    with pytest.raises(ValueError):
        league_rankings({})


def test_correct_league_standings_returned():
    teams = {'Bears': 7, 'Cats': 0, 'Dogs': 6, 'Cows': 1, 'Birds': 0}
    expected_standings = "1. Bears, 7 pts\n2. Dogs, 6 pts\n" \
                         "3. Cows, 1 pt\n4. Birds, 0 pts\n4. Cats, 0 pts"
    actual_standings = league_rankings(teams)
    assert expected_standings == actual_standings


def test_value_error_raised_when_no_output_args_provided():
    with pytest.raises(ValueError):
        write_output(output="", to_file=None, to_stdout=None)


def test_rankings_written_to_file():
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


def test_results_read_from_file():
    expected_input = ["Lions 3, Snakes 3", "Tarantulas 1, FC Awesome 0",
                      "Lions 1, FC Awesome 1", "Tarantulas 3, Snakes 1",
                      "Lions 4, Grouches 0"]
    actual_input = get_input(from_file="tests/sample_input.txt", from_stdin=None)
    assert expected_input == actual_input


def test_correct_rankings_returned():
    games = get_input(from_file="tests/sample_input.txt", from_stdin=None)
    teams = teams_with_points(games)
    actual_rankings = league_rankings(teams)

    expected_rankings = "1. Tarantulas, 6 pts\n2. Lions, 5 pts\n3. FC Awesome, 1 pt\n" \
                        "3. Snakes, 1 pt\n5. Grouches, 0 pts"
    assert actual_rankings == expected_rankings
