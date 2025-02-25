"""
Leaderboard and related dataclasses.

This module also includes functions for generating the leaderboards from a list of OnlineBotUser.
"""

import dataclasses

from src.generate.online_bot_user import OnlineBotUser, PerfType


@dataclasses.dataclass(frozen=True)
class LeaderboardBotInfo:
  """A translation of what is returned by the lichess API which is used as part of a row on the leaderboard."""

  # The bot's username
  username: str

  # The bot's rating for a particular PerfType
  rating: int

  # The number of games the bot has played for this PerfType
  games: int

  # The date the bot was created (YYYY-MM-DD)
  created_date: str

  # The date the bot was last seen (YYYY-MM-DD)
  last_seen_date: str

  @classmethod
  def create_bot_info_dict(cls, bot_user: OnlineBotUser) -> dict[PerfType, "LeaderboardBotInfo"]:
    """Convert an OnlineBotUser into a map from perf_type -> bot_info."""
    username = bot_user.username
    created_date = "TODO"
    last_seen_date = "TODO"

    bot_info_dict: dict[PerfType, LeaderboardBotInfo] = {}
    for perf in bot_user.perfs:
      bot_info_dict[perf.perf_type] = LeaderboardBotInfo(username, perf.rating, perf.games, created_date, last_seen_date)

    return bot_info_dict


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """
  A row in the leaderboard: rank, name, rating, etc...

  This class includes a LeaderboardBotInfo as well as additional details which are easier to calculate after the fact.
  """

  # Information about the bot returned by the lichess API
  bot_info: LeaderboardBotInfo

  # The bot's position within the leaderboard
  rank: int

  # How much their rank has changed since the last time the leaderboard was generated
  rank_delta: int

  # How much their rating has changed since the last time the leaderboard was generated
  rating_delta: int

  # The highest rank the bot has ever achieved on the leaderboard
  peak_rank: int

  # The maximum rating observed at any point when generating the leaderboard
  peak_rating: int

  @classmethod
  def create_leaderboard_rows(cls, bot_info_list: list[LeaderboardBotInfo]) -> list["LeaderboardRow"]:
    """
    Take a list of bot info and create a list of leaderboard rows.

    The resulting list is sorted by rating descending. This is a consequence of rank is determined (by sorting).

    rank_delta, rating_delta, peak_rank, and peak_rating all depend on what was within the leaderboard previously. As a result
    these are set to default values here and are expected to be updated later when we merge this list with an existing
    leaderboard.
    """
    # Primary sort: by rating descending, Secondary sort: creation date ascending
    sorted_bot_info_list = sorted(bot_info_list, key=lambda bot_info: (-bot_info.rating, bot_info.created_date))

    # The first in the list will be ranked #1
    rank = 1
    # No change for deltas since we have nothing to compare to (yet)
    rank_delta = 0
    rating_delta = 0

    leaderboard_rows: list[LeaderboardRow] = []
    for bot_info in sorted_bot_info_list:
      # The peaks become more interesting when comparing with a previous iteration of the leaderboard
      peak_rank = rank
      peak_rating = bot_info.rating
      leaderboard_rows.append(LeaderboardRow(bot_info, rank, rank_delta, rating_delta, peak_rank, peak_rating))
      # TODO: account for ties
      rank += 1

    return leaderboard_rows
