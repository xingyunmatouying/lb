# Lichess Bot Leaderboard

Automatically updating leaderboards for Lichess bots.

[Click here to view the leaderboards](https://eirik0.github.io/lichess-bot-leaderboard/).

## Overview

This project uses a
[GitHub Action to generate leaderboards](https://github.com/Eirik0/lichess-bot-leaderboard/blame/main/.github/workflows/generate-leaderboard.yaml)
once every 2 hours. The action runs a
[Python script which generates html](https://github.com/Eirik0/lichess-bot-leaderboard/blob/main/src/leaderboard/__main__.py)
which is then deployed as a GitHub Pages site. The data used to generate the leaderboards is provided by the
[Lichess get online bot API](https://lichess.org/api#tag/Bot/operation/apiBotOnline).

## Features

Here are some highlights of what this project does:

- Automatically updates once every two hours
- Generates leaderboards for all time controls and variants available to bots
- Uses [1224 ranking](<https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking)>) for handling
  ties
- Calculates deltas between prior runs for rank, rating, and games played
- Shows whether or not a bot was online when the leaderboard was last generated
- Shows whether or not a bot is a [Lichess Patron](https://lichess.org/patron)
- Indicates when a bot is new to the leaderboard
- Indicates when a previously ineligible bot returns to the leaderboard
- Displays flags using the [BabelStone Flags](https://www.babelstone.co.uk/Fonts/Flags.html) font
- Maintains a [complete history](https://github.com/Eirik0/lichess-bot-leaderboard/tree/leaderboard-pages/leaderboard_data) of
  the leaderboard data
- Has [CSS styling](https://github.com/Eirik0/lichess-bot-leaderboard/blob/main/leaderboard_html/css/style.css) which renders
  nicely on desktop and mobile

## Limitations

The leaderboards are static and the data does not change until the script which generates them runs again. The leaderboards
will not reflect changes to a bot's rating which occur in-between runs. Additionally, it is possible for bot's data to be
missed if they are not online at the exact moment when the leaderboards are generated.

## Generating the leaderboards locally

The leaderboard html will be output to the folder `leaderboard_html/`.

### Steps

This project is primarily written in [Python](https://www.python.org/downloads/) and assumes version 3.11 or greater.

Create a virtual environment

```shell
python -m venv .venv
```

Activate the environment

```shell
.venv\Scripts\activate # Windows cmd
```

```shell
.venv\Scripts\Activate.ps1 # Windows PowerShell
```

```shell
source .venv/bin/activate # MacOS and Linux
```

Install requirements

```shell
pip install -r requirements\leaderboard.txt
```

Generate the leaderboards

```shell
python -m src.leaderboard
```

## Development

This project was developed in VS Code. The repo contains several recommended extensions to aid in development.

### CI

The CI for this project includes several checks which are configured as GitHub actions. All of these can be performed locally,
too.

#### **Setup**

Begin following the same steps as above.

1. Create a virtual environment
2. Activate the environment
3. Install all requirements to generate the leaderboards as well as for linting, formatting, and code coverage

```shell
pip install -r requirements\all.txt
```

#### **Check linting and formatting**

Python

```shell
ruff format --check  # Check format
```

```shell
ruff check           # Check lint
```

Jinja

```shell
djlint templates -e jinja --check  # Check format
```

```shell
djlint templates -e jinja --lint   # Check lint
```

#### **Check types**

Install pyright with npm

```shell
npm install -g pyright
```

Run static type checking

```shell
pyright --verbose
```

Alternatively this can be done from within VS Code.

#### **Run tests**

The following command runs tests in the `tests` directory which match the pattern `test_*.py`

```shell
python -m unittest discover -v -s tests -p test_*.py
```

#### **Run code coverage**

The `coverage run` command is configured to use the same command as above when running tests.

```shell
coverage run   # Generate the coverage file
```

```shell
coverage html  # Generate coverage html
```

```shell
coverage xml   # Generate coverage xml
```
