"""Leaderboard-related dataclasses."""

import dataclasses
import json
from typing import Any

from src.leaderboard.li.bot_user import BotUser, Perf


@dataclasses.dataclass(frozen=True)
class LeaderboardPerf:
  """A bot's performance for a particular PerfType.

  The performance type is not stored within this object itself.

  This also contains some additional information about the bot.
  """

  # The bot's username
  username: str
  # The bot's flair
  flair: str
  # The bot's country flag
  flag: str
  # The bot's rating
  rating: int
  # The bot's rating deviation
  rd: int
  # The bot's rating change (progress) over the last 12 games
  prog: int
  # The number of games the bot has played
  games: int
  # The date the bot was created (YYYY-MM-DD)
  created_date: str
  # The date the bot was last seen (YYYY-MM-DD)
  last_seen_date: str
  # If the bot is a patron
  patron: bool
  # If the bot has violated the terms of service
  tos_violation: bool

  @classmethod
  def from_bot_user(cls, bot_user: BotUser, perf: Perf, last_seen_date: str) -> "LeaderboardPerf":
    """Create a leaderboard perf from a bot user and a perf."""
    return LeaderboardPerf(
      bot_user.username,
      bot_user.flair,
      bot_user.flag,
      perf.rating,
      perf.rd,
      perf.prog,
      perf.games,
      bot_user.created_date,
      last_seen_date,
      bot_user.patron,
      bot_user.tos_violation,
    )

  @classmethod
  def from_json(cls, json_dict: dict[str, Any]) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from json."""
    username = json_dict.get("username", "")
    flair = json_dict.get("flair", "")
    flag = json_dict.get("flag", "")
    rating = json_dict.get("rating", 0)
    rd = json_dict.get("rd", 0)
    prog = json_dict.get("prog", 0)
    games = json_dict.get("games", 0)
    created_date = json_dict.get("created_date", "")
    last_seen_date = json_dict.get("last_seen_date", "")
    patron = json_dict.get("patron", False)
    tos_violation = json_dict.get("tos_violation", False)
    return LeaderboardPerf(username, flair, flag, rating, rd, prog, games, created_date, last_seen_date, patron, tos_violation)


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """A row in the leaderboard: rank, name, rating, etc...

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
  # Whether or not this is the bots first time on the leaderboard
  is_new: bool
  # Whether or not the bot was online when the leaderboard was generated
  is_online: bool

  @classmethod
  def from_json(cls, json_str: str) -> "LeaderboardRow":
    """Create a LeaderboardRow from json."""
    json_dict = json.loads(json_str)

    perf_dict = json_dict.get("perf", {})
    perf = LeaderboardPerf.from_json(perf_dict)

    rank = json_dict.get("rank", 0)
    rank_delta = json_dict.get("rank_delta", 0)
    rating_delta = json_dict.get("rating_delta", 0)
    peak_rank = json_dict.get("peak_rank", 0)
    peak_rating = json_dict.get("peak_rating", 0)
    is_new = json_dict.get("is_new", False)
    is_online = json_dict.get("is_online", False)

    return LeaderboardRow(perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, is_new, is_online)

  def to_json(self) -> str:
    """Convert the leaderboard row to."""
    self_as_dict = dataclasses.asdict(self)
    return json.dumps(self_as_dict)
