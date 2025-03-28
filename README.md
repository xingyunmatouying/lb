# Lichess Bot Leaderboard

Automatically updating Lichess bot leaderboards.

## Overview

This is a python script which queries the Lichess API for online bots. Using the online bot data, combined with data from prior
runs, it outputs html files which contain leaderboards for all Lichess time controls and variants available to bots.

## Generating the leaderboards locally

The leaderboard html will be output to the folder `leaderboard_html`.

### Installation

Create a virtual environment

```shell
python -m venv .venv
```

Activate the environment

```shell
.venv\Scripts\activate      # Windows cmd
```

```shell
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

```shell
source .venv/bin/activate   # MacOS and Linux
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
