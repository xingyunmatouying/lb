"""
Leaderboard and related dataclasses.

This module also includes functions for generating the leaderboards from a list of OnlineBotUser.
"""

import dataclasses

from src.generate.online_bot_user import OnlineBotUser, Perf


@dataclasses.dataclass(frozen=True)
class LeaderboardPerf:
  """
  A bots performance for a known PerfType.

  The performance type is not stored within this object itself.

  This also contains some additional information about the bot.
  """

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
  def from_online_bot_user(cls, online_bot_user: OnlineBotUser, perf: Perf) -> "LeaderboardPerf":
    """Create a leaderboard perf from a bot user and a perf."""
    return LeaderboardPerf(online_bot_user.username, perf.rating, perf.games, "TODO", "TODO")


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """
  A row in the leaderboard: rank, name, rating, etc...

  This class includes a LeaderboardPerf as well as additional details which are easier to calculate after the fact.
  """

  # Information about the bot returned by the lichess API
  perf: LeaderboardPerf

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
  def from_psv(cls, psv_string: str) -> "LeaderboardRow":
    """Create a LeaderboardRow based on pipe separated values."""
    values = psv_string.split("|")

    username = values[0]
    rating = int(values[1])
    games = int(values[2])
    created_date = values[3]
    last_seen_date = values[4]
    perf = LeaderboardPerf(username, rating, games, created_date, last_seen_date)

    rank = int(values[5])
    rank_delta = int(values[6])
    rating_delta = int(values[7])
    peak_rank = int(values[8])
    peak_rating = int(values[9])

    return LeaderboardRow(perf, rank, rank_delta, rating_delta, peak_rank, peak_rating)

  @classmethod
  def create_leaderboard_rows(cls, perf_list: list[LeaderboardPerf]) -> list["LeaderboardRow"]:
    """
    Take a list of bot info and create a list of leaderboard rows.

    The resulting list is sorted by rating descending. This is a consequence of rank is determined (by sorting).

    rank_delta, rating_delta, peak_rank, and peak_rating all depend on what was within the leaderboard previously. As a result
    these are set to default values here and are expected to be updated later when we merge this list with an existing
    leaderboard.
    """
    # Primary sort: by rating descending, Secondary sort: creation date ascending
    sorted_perf_list = sorted(perf_list, key=lambda perf: (-perf.rating, perf.created_date))

    # The first in the list will be ranked #1
    rank = 0
    # No change for deltas since we have nothing to compare to (yet)
    rank_delta = 0
    rating_delta = 0

    # Used for 1224 ranking (https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking))
    same_rank_count = 0
    previous_rating = 0

    leaderboard_rows: list[LeaderboardRow] = []
    for perf in sorted_perf_list:
      if perf.rating == previous_rating:
        same_rank_count += 1
      else:
        rank += same_rank_count
        rank += 1
        same_rank_count = 0
      # The peaks become more interesting when comparing with a previous iteration of the leaderboard
      peak_rank = rank
      peak_rating = perf.rating
      leaderboard_rows.append(LeaderboardRow(perf, rank, rank_delta, rating_delta, peak_rank, peak_rating))
      previous_rating = perf.rating

    return leaderboard_rows
