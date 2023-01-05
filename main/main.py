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


def _rank_formatter(rank: int, name: str, points: int, carriage_return: bool) -> str:
    pts = "pt" if points == 1 else "pts"
    pts = f"{pts}\n" if carriage_return else pts
    return f"{rank}. {name}, {points} {pts}"


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


def league_rankings(teams_with_points: dict) -> str:
    if not teams_with_points:
        raise ValueError("No teams with points found")
    sorted_teams = sorted(teams_with_points.items(), key=lambda x: x[1], reverse=True)
    num_teams_placed = len(sorted_teams)
    rank = 1
    prev = None
    ranks = ""
    for team in sorted_teams:
        name, points = team
        if prev is not None:
            current_team_points = teams_with_points.get(name)
            prev_team_points = teams_with_points.get(prev)
            if current_team_points == prev_team_points:
                rank -= 1
        ranks += _rank_formatter(rank, name, points, num_teams_placed > 1)
        rank += 1
        prev = name
        num_teams_placed -= 1
    return ranks


if __name__ == '__main__':
    sample_input = "Lions 3, Snakes 0|Tarantulas 3, FC Awesome 0|Lions 1, FC Awesome 1|Tarantulas 3, Snakes 0|Lions 3, Grouches 0"
    games = sample_input.split("|")
    teams = defaultdict(int)
    for game in games:
        for team in match_result(game):
            teams[team.name] += team.points
    # 1. Lions, 7 pts
    # 2. Tarantulas, 6 pts
    # 3. FC Awesome, 1 pt
    # 4. Grouches, 0 pts
    # 4. Snakes, 0 pts
    standings = league_rankings(teams)
    print(standings)

