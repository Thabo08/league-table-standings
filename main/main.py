

from collections import defaultdict
from collections import namedtuple
from typing import Any
from typing import Tuple

Team = namedtuple("Team", "name points")


def _individual_result(team_result: str) -> Team:
    team_result = team_result.strip()  # remove any leading or trailing spaces
    if len(team_result.split(" ")) < 2:
        raise ValueError(f"{team_result} is of invalid format. Expected format is: 'Team1 3'")

    last_index_of_space = team_result.rindex(" ")
    team_name = team_result[:last_index_of_space]
    try:
        points = int(team_result[-1])
    except ValueError:
        # raised if str cannot be converted to int type
        raise
    return Team(team_name, points)


def match_result(game_result: Any) -> Tuple[Team, Team]:
    if game_result is None:
        raise ValueError("Invalid input. Value cannot be None")
    if game_result == "":
        raise ValueError("Invalid input. Value cannot be empty")

    match = game_result.split(",")
    if len(match) != 2:
        raise ValueError(f"{game_result} format is invalid. Expected format is: 'Team1 3, Team2 0'")

    team_1, team_2 = match
    return _individual_result(team_1), _individual_result(team_2)


if __name__ == '__main__':
    sample_input = "Lions 3, Snakes 3|Tarantulas 1, FC Awesome 0|Lions 1, FC Awesome 1|Tarantulas 3, Snakes 1|Lions 4, Grouches 0"
    results = sample_input.split("|")
    teams = defaultdict(int)
    for result in results:
        team_1, team_2 = match_result(result)
        teams[team_1.name] += team_1.points
        teams[team_2.name] += team_2.points

    print(teams)
