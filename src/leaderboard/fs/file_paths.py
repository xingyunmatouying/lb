"""Module containing functions to get leaderboard file paths."""

from src.leaderboard.li.pert_type import PerfType


def bot_profiles_path() -> str:
  """Return "leaderboard_data/bot_profiles.ndjson"."""
  return "leaderboard_data/bot_profiles.ndjson"


def data_path(perf_type: PerfType) -> str:
  """Return "leaderboard_data/{perf_type.to_string()}.ndjson"."""
  return f"leaderboard_data/{perf_type.to_string()}.ndjson"


def html_path(name: str) -> str:
  """Return "leaderboard_html/{name}.html"."""
  return f"leaderboard_html/{name}.html"
