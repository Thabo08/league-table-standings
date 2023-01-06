[![build](https://github.com/Thabo08/movie-service/actions/workflows/main.yaml/badge.svg)](https://github.com/Thabo08/movie-service/actions/workflows/main.yaml)
# League Table Standings

This app calculates league table standings based on the results of the game between two teams. The rankings
are based on a points system. Each team is allocated points based on how it performed against its opponent. If two
teams scored the same number of goals against each other (a draw), they each receive **1 point**, if not, then the team
which scored the most goals (winner) gets **3 points** and the other team (loser) gets **0 points**.

The app reads game results either from file or from command line and writes the league standings either to file or
to the console. The app can be ran in one of the following ways:

### Usage
1. Print usage/help menu:
   ```
   python main/main.py -h
   ```
2. Take input from file* and write results to file
    ```commandline
    python main/main.py --fileinput {INPUT_FILE_PATH} --fileoutput {OUTPUT_FILE_PATH}
    ```
3. Take input from file* and write results to console
    ```commandline
    python main/main.py --fileinput {INPUT_FILE_PATH} --cmdoutput
    ```
4. Take input from console** in pipe delimited format and write results to file
    ```commandline
    python main/main.py --cmdinput "Lions 3, Bears 0 | Cats 1, Dogs 1" --fileoutput {OUTPUT_FILE_PATH}
    ```
5. Take input from console** and write results to console
    ```commandline
    python main/main.py --cmdinput "Lions 3, Bears 0 | Cats 1, Dogs 1" --cmdoutput
    ```

*Contents of the input file provided are in the following format, where each line is the results of 
the game between two teams:
```text
   Lions 3, Bears 0
   Cats 1, Dogs 1
```
**Contents from the command line are in the following format, where the pipe ```|``` separates two
games between teams:
```text
   Lions 3, Bears 0 | Cats 1, Dogs 1
```

### Installing Dependencies
Package dependencies can be installed using ```pip install -r {path_to_requirements_file}```

### Unit Testing
Unit tests can be ran using ```python -m pytest -s tests``` when in the base directory of the project.

### Code Formatting
Code can be formatted using ```python -m black .``` when in the base directory of the project.
