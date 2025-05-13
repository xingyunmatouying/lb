"""Module containing functions to get leaderboard file paths."""

from src.leaderboard.li.pert_type import PerfType


LEADERBOARD_DATA_DIR = "leaderboard_data"


def bot_profiles_path() -> str:
  """Return "leaderboard_data/bot_profiles.json"."""
  return f"{LEADERBOARD_DATA_DIR}/bot_profiles.json"


def data_path(perf_type: PerfType) -> str:
  """Return "leaderboard_data/{perf_type.to_string()}.json"."""
  return f"{LEADERBOARD_DATA_DIR}/{perf_type.to_string()}.json"


def generation_number_path() -> str:
  """Return "leaderboard_data/generation_number.txt"."""
  return f"{LEADERBOARD_DATA_DIR}/generation_number.txt"


def html_path(name: str) -> str:
  """Return "leaderboard_html/{name}.html"."""
  return f"leaderboard_html/{name}.html"
