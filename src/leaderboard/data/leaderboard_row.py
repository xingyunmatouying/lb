"""Dataclasses related rows in a leaderboard."""

import dataclasses
import json
from typing import Any

from src.leaderboard.li.bot_user import BotUser, Perf


@dataclasses.dataclass(frozen=True)
class BotProfile:
  """Information related to the bot's profile.

  This is information that either never changes or does not change very often.
  """

  # The bot's username
  username: str
  # The bot's flair
  flair: str
  # The bot's country flag
  flag: str
  # The date the bot was created (YYYY-MM-DD)
  created_date: str
  # If the bot is a patron
  patron: bool
  # If the bot has violated the terms of service
  tos_violation: bool

  @classmethod
  def from_bot_user(cls, bot_user: BotUser) -> "BotProfile":
    """Create a BotProfile from a BotUser."""
    return BotProfile(
      bot_user.username, bot_user.flair, bot_user.flag, bot_user.created_date, bot_user.patron, bot_user.tos_violation
    )

  @classmethod
  def from_json(cls, json_dict: dict[str, Any]) -> "BotProfile":
    """Create a BotProfile from json."""
    return BotProfile(
      json_dict.get("username", ""),
      json_dict.get("flair", ""),
      json_dict.get("flag", ""),
      json_dict.get("created_date", ""),
      json_dict.get("patron", False),
      json_dict.get("tos_violation", False),
    )


@dataclasses.dataclass(frozen=True)
class LeaderboardPerf:
  """Information related to a bot's performance for a particular PerfType.

  The performance type is not stored within this object itself.
  """

  # The bot's rating
  rating: int
  # The bot's rating deviation
  rd: int
  # The bot's rating change (progress) over the last 12 games
  prog: int
  # The number of games the bot has played
  games: int

  @classmethod
  def from_perf(cls, perf: Perf) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from a Perf."""
    return LeaderboardPerf(perf.rating, perf.rd, perf.prog, perf.games)

  @classmethod
  def from_json(cls, json_dict: dict[str, Any]) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from json."""
    return LeaderboardPerf(
      json_dict.get("rating", 0), json_dict.get("rd", 0), json_dict.get("prog", 0), json_dict.get("games", 0)
    )


@dataclasses.dataclass(frozen=True)
class BotInfo:
  """Information about the bot which may appear on the leaderboard."""

  # Information related to the bot's profile.
  profile: BotProfile
  # Information related to a bot's performance for a particular PerfType.
  perf: LeaderboardPerf
  # The date the bot was last seen (YYYY-MM-DD)
  last_seen_date: str

  @classmethod
  def create_bot_info(cls, bot_user: BotUser, perf: Perf, last_seen_date: str) -> "BotInfo":
    """Create a BotInfo from information returned by the lichess API."""
    return BotInfo(BotProfile.from_bot_user(bot_user), LeaderboardPerf.from_perf(perf), last_seen_date)

  @classmethod
  def from_json(cls, json_dict: dict[str, Any]) -> "BotInfo":
    """Create a BotInfo from json."""
    return BotInfo(
      BotProfile.from_json(json_dict.get("profile", {})),
      LeaderboardPerf.from_json(json_dict.get("perf", {})),
      json_dict.get("last_seen_date", ""),
    )


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """A row in the leaderboard: rank, name, rating, etc...

  This class includes a BotInfo as well as additional details which are calculated.
  """

  # Information about the bot returned by the lichess API
  bot_info: BotInfo
  # The bot's position within the leaderboard
  rank: int
  # How much their rank has changed since the last time the leaderboard was generated
  delta_rank: int
  # How much their rating has changed since the last time the leaderboard was generated
  delta_rating: int
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
    return LeaderboardRow(
      BotInfo.from_json(json_dict.get("bot_info", {})),
      json_dict.get("rank", 0),
      json_dict.get("delta_rank", 0),
      json_dict.get("delta_rating", 0),
      json_dict.get("peak_rank", 0),
      json_dict.get("peak_rating", 0),
      json_dict.get("is_new", False),
      json_dict.get("is_online", False),
    )

  def to_json(self) -> str:
    """Convert the leaderboard row to."""
    self_as_dict = dataclasses.asdict(self)
    return json.dumps(self_as_dict)
