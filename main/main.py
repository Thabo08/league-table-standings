import argparse
from collections import defaultdict
from collections import namedtuple
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple


class RankManager:
    """Helper class to manage rankings."""
    def __init__(self):
        self.current_rank = 0
        self.previous_rank = 0

    def get_rank(self, same_points=False):
        self.current_rank += 1
        if same_points:
            return self.previous_rank
        else:
            self.previous_rank = self.current_rank
            return self.current_rank


Team = namedtuple("Team", "name points")


def _individual_result(team_result: str) -> dict[str, int]:
    team_result = team_result.strip()  # remove any leading or trailing spaces
    if len(team_result.split(" ")) < 2:
        raise ValueError(f"{team_result} is of invalid format. Expected format is: 'Team1 3'")

    last_index_of_space = team_result.rindex(" ")
    team_name = team_result[:last_index_of_space]
    try:
        goals = int(team_result[-1])
    except ValueError:
        # raised if str cannot be converted to int type
        raise
    return {"name": team_name, "goals": goals}


def _rank_formatter(rank: int, name: str, points: int, carriage_return: bool) -> str:
    pts = "pt" if points == 1 else "pts"
    pts = f"{pts}\n" if carriage_return else pts
    return f"{rank}. {name}, {points} {pts}"


def _points_allocator(team_1_goals: int, team_2_goals: int) -> Tuple[int, int]:
    if team_1_goals != team_2_goals:
        team_1_points = 3 if team_1_goals > team_2_goals else 0
        team_2_points = 3 if team_2_goals > team_1_goals else 0
        return team_1_points, team_2_points
    return 1, 1


def match_points(game_result: Any) -> Tuple[Team, Team]:
    """ Takes a game result and returns teams with points based on the result.

        e.g For result 'Lions 4, Grouches 0', Team(Lions, 3), Team(Grouches, 0)
        will be returned as Lions beat the Grouches

        Args:
            game_result: game result in string format, eg, 'Lions 4, Grouches 0'

        Returns:
            Tuple of Team objects with points based on the game results
    """
    if game_result is None or game_result == "":
        raise ValueError("Invalid input. Value cannot be None or empty")

    match = game_result.split(",")
    if len(match) != 2:
        raise ValueError(f"{game_result} format is invalid. Expected format is: 'Team1 3, Team2 0'")

    team_1_result, team_2_result = match
    team_1 = _individual_result(team_1_result)
    team_2 = _individual_result(team_2_result)
    team_1_goals, team_2_goals = team_1.get("goals"), team_2.get("goals")
    team_1_points, team_2_points = _points_allocator(team_1_goals, team_2_goals)
    return Team(team_1.get("name"), team_1_points), Team(team_2.get("name"), team_2_points)


def league_rankings(teams_with_points: dict) -> str:
    if not teams_with_points:
        raise ValueError("No teams with points found")
    sorted_teams = sorted(teams_with_points.items(), key=lambda x: x[1])
    num_teams_placed = len(sorted_teams)
    rank_manager = RankManager()
    prev = None
    ranks = ""
    for i in range(len(sorted_teams) - 1, -1, -1):
        name, points = sorted_teams[i]
        same_points = False
        if prev is not None:
            current_team_points = teams_with_points.get(name)
            prev_team_points = teams_with_points.get(prev)
            same_points = current_team_points == prev_team_points
        rank = rank_manager.get_rank(same_points)
        ranks += _rank_formatter(rank, name, points, num_teams_placed > 1)
        prev = name
        num_teams_placed -= 1
    return ranks


def write_output(output: str, to_file: Optional[str], to_stdout: Optional[str]):
    def write_to_file(filename, contents):
        with open(filename, "w") as f:
            f.write(contents)

    if to_file and to_stdout:
        print(output)
        write_to_file(to_file, output)
    elif to_file and not to_stdout:
        write_to_file(to_file, output)
    elif not to_file and to_stdout:
        print(output)
    else:
        raise ValueError("Specify at least one output target")


def get_input(from_file: Optional[str], from_stdin: Optional[str]) -> List[str]:
    if from_file and from_stdin:
        # just get from stdin
        return from_stdin.split("|")
    elif from_file and not from_stdin:
        contents = []
        with open(from_file) as f:
            for line in f.readlines():
                contents.append(line.strip())
        return contents
    elif not from_file and from_stdin:
        return from_stdin.split("|")
    else:
        raise ValueError("Specify at least one input source")


def _cmd_args():
    global args
    parser = argparse.ArgumentParser(description="This program accepts results of games either "
                                                 "as stdin or filename and outputs the league "
                                                 "rankings either to stdout or file")
    parser.add_argument("--fileinput", help="Input file containing the game results")
    parser.add_argument("--cmdinput", help="Receive results from stdin")
    parser.add_argument("--fileoutput", help="Output file containing the league rankings")
    parser.add_argument("--cmdoutput", help="Print rankings to stdout", action="store_true")

    return parser.parse_args()


def teams_with_points(games: List[str]) -> dict:
    teams = defaultdict(int)
    for game in games:
        for team in match_points(game):
            teams[team.name] += team.points
    return teams


if __name__ == '__main__':
    args = _cmd_args()
    games = get_input(from_file=args.fileinput, from_stdin=args.cmdinput)
    teams = teams_with_points(games)
    rankings = league_rankings(teams)
    write_output(output=rankings, to_file=args.fileoutput, to_stdout=args.cmdoutput)

    # sample input
    # "Lions 3, Snakes 0|Tarantulas 3, FC Awesome 0|Lions 1, FC Awesome 1|Tarantulas 3, Snakes 0|Lions 3, Grouches 0"

    # sample output
    # 1. Tarantulas, 6 pts
    # 2. Lions, 5 pts
    # 3. FC Awesome, 1 pt
    # 3. Snakes, 1 pt
    # 5. Grouches, 0 pts
