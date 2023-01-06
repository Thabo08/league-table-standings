import argparse
from typing import List
from typing import Optional

from rank_teams import league_rankings
from rank_teams import teams_with_points


# File Operation functions
def write_output(output: str, to_file: Optional[str], to_stdout: Optional[str]):
    """Writes output to file or to console

    Args:
        output: Data to be written
        to_file: Path to file to be written to
        to_stdout: Flag to decide whether or not to write to console
    """

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
    """Reads input from file or console

    Args:
        from_file: File containing input to read
        from_stdin: Data pass from console

    Return:
        A list of game results read either from file or the console
    """
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


# End of File Operation functions


def _cmd_args():
    """Configure args used when running the program in the command line"""
    parser = argparse.ArgumentParser(
        description="This program accepts results of games either "
        "as stdin or filename and outputs the league "
        "rankings either to stdout or file"
    )
    parser.add_argument(
        "--fileinput", type=str, help="Input file containing the game results"
    )
    parser.add_argument("--cmdinput", type=str, help="Receive results from stdin")
    parser.add_argument(
        "--fileoutput", type=str, help="Output file containing the league rankings"
    )
    parser.add_argument(
        "--cmdoutput", help="Print rankings to stdout", action="store_true"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _cmd_args()
    games = get_input(from_file=args.fileinput, from_stdin=args.cmdinput)
    teams = teams_with_points(games)
    rankings = league_rankings(teams)
    write_output(output=rankings, to_file=args.fileoutput, to_stdout=args.cmdoutput)
