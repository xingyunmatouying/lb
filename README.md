# lichess-bot-leaderboard

## Installation

### Windows

#### Create a virtual environment

    python -m venv .venv

#### Activate the environment

    .venv\Scripts\activate # cmd

or

    .venv\Scripts\Activate.ps1 # powershell

#### Install development dependencies

    pip install -r requirements.txt

## How to use

### Generate the leaderboard

    python -m src.generate

## Testing

Run tests in the `tests` directory which match the pattern `test_*.py`

    python -m unittest discover -v -s tests -p test_*.py
