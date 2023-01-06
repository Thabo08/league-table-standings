import pytest

from main.main import get_input
from main.main import write_output


class TestFileInputAndOutput:
    def test_value_error_raised_when_no_output_args_provided(self):
        with pytest.raises(ValueError):
            write_output(output="", to_file=None, to_stdout=None)

    def test_rankings_written_to_file(self):
        import os

        expected_standings = (
            "1. Team3, 7 pts\n2. Team4, 6 pts\n"
            "3. Team2, 1 pt\n4. Team1, 0 pts\n4. Team5, 0 pts"
        )
        write_output(expected_standings, to_file="sample_output.txt", to_stdout=None)
        with open("sample_output.txt") as f:
            file_contents = f.read()
        try:
            os.remove("sample_output.txt")
        except Exception:
            pass

        assert expected_standings == file_contents

    def test_value_error_raised_when_no_input_args_provided(self):
        with pytest.raises(ValueError):
            get_input(from_file=None, from_stdin=None)

    def test_results_read_from_file(self):
        expected_input = [
            "Lions 3, Snakes 3",
            "Tarantulas 1, FC Awesome 0",
            "Lions 1, FC Awesome 1",
            "Tarantulas 3, Snakes 1",
            "Lions 4, Grouches 0",
        ]
        actual_input = get_input(from_file="tests/sample_input.txt", from_stdin=None)
        assert expected_input == actual_input
