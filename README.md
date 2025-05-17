# Lichess Bot Leaderboard

Automatically updating leaderboards for [Lichess bots](https://lichess.org/player/bots).

[Click here to view the leaderboards](https://eirik0.github.io/lichess-bot-leaderboard).

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

## Leaderboard Eligibility

Eligibility for these leaderboards differs somewhat from the
[Lichess human leaderboard requirements](https://lichess.org/faq#leaderboards). For a bot to be eligible, they must:

1. have appeared online in the last 2 weeks
2. have played a game for the time control or variant in the last 2 weeks
3. not have a [provisional rating](https://lichess.org/faq#provisional)
4. not have violated the TOS

## Generating the leaderboards locally

It is possible to generate the leaderboards locally. After running the script, the leaderboard html will be output to the
folder `leaderboard_html/`.

### Steps

This project is primarily written in [Python](https://www.python.org/downloads) and assumes version 3.11 or greater.

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

Contributions to this project are welcome!

This project was developed in [VS Code](https://code.visualstudio.com). This repository includes workspace settings and several
recommended extensions to aid in development.

### **Setup**

Begin following the same steps as above.

1. Create a virtual environment
2. Activate the environment
3. Install the dev requirements

```shell
pip install -r requirements\all.txt
```

### **Testing**

The easiest way to run the tests is by running them with code coverage.

```shell
coverage run # Run the tests and generate code coverage
```

To view the coverage html, also run the following and then check the output in `htmlcov/`

```shell
coverage html  # Generate coverage html
```

### **CI**

The CI for this project includes several checks which are configured as a
[GitHub Actions CI workflow](https://github.com/Eirik0/lichess-bot-leaderboard/blob/main/.github/workflows/ci.yaml). Much of
the linting and formatting is handled automatically when using the recommended VS Code extensions, but it can all be performed
from the command line, too.

#### **Optional Additional Setup**

To run all of the linting and formatting from the command line, some additional setup is needed. While this is not required,
some of the VS Code extensions work better if the linter or formatter is also installed locally.

Some of the linting and formatting is handled by [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
packages.

```shell
npm install # Install dev dependencies
```

Also install [Taplo](https://taplo.tamasfe.dev/cli/installation/binary.html). Taplo seemed to work best when installed
precompiled rather than via a package manager.

#### **Check linting and formatting**

Here are all of the checks which are run by the CI.

```shell
npx prettier . --check --log-level debug # formatting (css, json, md, yaml)

npx stylelint **/*.css --ignore-path .gitignore --formatter verbose # linting (css)

djlint templates --extension jinja --lint # linting (jinja)
djlint templates --extension jinja --check # formatting (jinja)

npx markdownlint-cli2 "**/*.md" # linting (markdown)

ruff format --check --verbose # formatting (python)
ruff check --verbose # linting (python)

npx pyright --verbose # static type checking (python)

taplo fmt --check # formatting (toml)
taplo check # linting (toml)
```

## Acknowledgements

This project drew inspiration from the following sources at various times during its development:

- [Lichess](https://github.com/lichess-org)
- [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot)
- [python-chess](https://github.com/niklasf/python-chess)
- [ruff](https://github.com/astral-sh/ruff)
- [Live Chess Ratings (2700chess.com)](https://2700chess.com) (Ad warning)
- [Gemini](https://gemini.google.com)
