# (Unofficial) Lichess Bot Leaderboard

## Installation (Windows)

1. Create a virtual environment

    ```shell
    python -m venv .venv
    ```

2. Activate the environment

    ```shell
    .venv\Scripts\activate # cmd
    ```

    or

    ```shell
    .venv\Scripts\Activate.ps1 # powershell
    ```

3. Install requirements

    ```shell
    pip install -r requirements\leaderboard.txt
    ```

4. Generate the leaderboards

    ```shell
    python -m src.generate
    ```

## Development

### Installation

1. Create a virtual environment
2. Activate the environment
3. Install all requirements to generate the leaderboards as well as for linting, formatting, and code coverage

    ```shell
    pip install -r requirements\all.txt
    ```

### Check linting and formatting

- Check formatting

    ```shell
    ruff format --check
    ```

- Check linting

    ```shell
    ruff check
    ```

### Run tests

- Run tests in the `tests` directory which match the pattern `test_*.py`

    ```shell
    python -m unittest discover -v -s tests -p test_*.py
    ```

### Generate code coverage

- Generate the coverage file

    This is configured to use the same command as when running tests

    ```shell
    coverage run
    ```

- Generate coverage html

    ```shell
    coverage html
    ```

- Generate coverage xml

    ```shell
    coverage xml
    ```
