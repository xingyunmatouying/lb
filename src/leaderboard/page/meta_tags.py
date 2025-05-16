"""Module containing functions for creating content for html meta tags."""

from src.leaderboard.li.pert_type import PerfType


def get_description(perf_type: PerfType | None) -> str:
  """Create content for the "description" tag."""
  description_lines = (
    [
      f"Automatically updated Lichess bot {perf_type.get_readable_name()} leaderboard.",
      f"Rankings for the top {perf_type.get_readable_name()} bots on Lichess.",
    ]
    if perf_type
    else [
      "Automatically updated Lichess bot leaderboards.",
      "Rankings for the top Lichess bots for each time control and variant.",
    ]
  )
  return " ".join(description_lines)


def get_keywords(perf_type: PerfType | None) -> str:
  """Create content for the "keywords" tag."""
  keywords: list[str] = (
    [
      f"{perf_type.get_readable_name()} bot leaderboard",
      f"best bot at {perf_type.get_readable_name()}",
      f"top {perf_type.get_readable_name()} bot",
      f"Lichess bot {perf_type.get_readable_name()} rankings",
      f"Lichess {perf_type.get_readable_name()} bot",
      f"Lichess bot {perf_type.get_readable_name()} leaderboard",
    ]
    if perf_type
    else [
      "Lichess bot leaderboard",
      "best bot on Lichess",
      "top Lichess bot",
      "Lichess bot rankings",
    ]
    + [f"{perf_type.get_readable_name()} leaderboard" for perf_type in PerfType.all_except_unknown()]
  )
  return ", ".join(keywords)
