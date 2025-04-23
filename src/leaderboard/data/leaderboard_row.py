"""Dataclasses related rows in a leaderboard."""

import dataclasses
import json
from typing import Any

from src.leaderboard.data import default_remover
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
  # The time the bot was created (seconds since epoch)
  created_time: int
  # The time the bot was last seen (seconds since epoch)
  last_seen_time: int
  # If the bot is a patron
  patron: bool
  # If the bot has violated the terms of service
  tos_violation: bool
  # Whether or not this is the bot's first time on the leaderboard
  is_new: bool
  # Whether or not the bot was online when the leaderboard was generated
  is_online: bool

  @classmethod
  def from_bot_user(cls, bot_user: BotUser, last_seen_time: int) -> "BotProfile":
    """Create a BotProfile from a BotUser.

    The bot will be assumed to be new and to be online.
    """
    return BotProfile(
      bot_user.username,
      bot_user.flair,
      bot_user.flag,
      bot_user.created_at,
      last_seen_time,
      bot_user.patron,
      bot_user.tos_violation,
      # Assume the bot is new - this simplifies updates
      True,
      # If we are creating a BotProfile from a BotUser then the bot is online
      True,
    )

  @classmethod
  def from_json(cls, json_str: str) -> "BotProfile":
    """Create a BotProfile from json.

    The bot will be assumed not to be new and to be offline.
    """
    return BotProfile.from_json_dict(json.loads(json_str))

  @classmethod
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "BotProfile":
    """Create a BotProfile from a json dict.

    The bot will be assumed not to be new and to be offline.
    """
    return BotProfile(
      json_dict.get("username", ""),
      json_dict.get("flair", ""),
      json_dict.get("flag", ""),
      json_dict.get("created_time", 0),
      json_dict.get("last_seen_time", 0),
      json_dict.get("patron", False),
      json_dict.get("tos_violation", False),
      # If we are loading from json the bot is not new
      False,
      # Assume the bot is offline - this simplifies updates
      False,
    )

  def create_updated_copy_for_for_merge(self) -> "BotProfile":
    """Create an updated copy of the profile.

    The updated copy has is_new set to False and is_online set to True.
    """
    return BotProfile(
      self.username,
      self.flair,
      self.flag,
      self.created_time,
      self.last_seen_time,
      self.patron,
      self.tos_violation,
      False,
      True,
    )

  def to_json(self) -> str:
    """Convert the BotProfile to json.

    Values will only be set if they are not equal to their default values.
    """
    return json.dumps(default_remover.to_dict_without_defaults(dataclasses.asdict(self)))


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
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from a json dict."""
    return LeaderboardPerf(
      json_dict.get("rating", 0), json_dict.get("rd", 0), json_dict.get("prog", 0), json_dict.get("games", 0)
    )


@dataclasses.dataclass(frozen=True)
class BotPerf:
  """A pair of bot username and LeaderboardPerf."""

  username: str
  perf: LeaderboardPerf


@dataclasses.dataclass(frozen=True)
class RankInfo:
  """Information related to the bot's rank in the leaderboard row."""

  # The bot's rank on the leaderboard
  rank: int
  # How much their rank has changed since the last time the leaderboard was generated
  delta_rank: int
  # How much their rating has changed since the last time the leaderboard was generated
  delta_rating: int
  # The highest rank the bot has ever achieved on the leaderboard
  peak_rank: int
  # The maximum rating observed at any point when generating the leaderboard
  peak_rating: int

  @classmethod
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "RankInfo":
    """Create a RankInfo from a json dict."""
    return RankInfo(
      json_dict.get("rank", 0),
      json_dict.get("delta_rank", 0),
      json_dict.get("delta_rating", 0),
      json_dict.get("peak_rank", 0),
      json_dict.get("peak_rating", 0),
    )


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """Data that is specific to a row on a particular leaderboard."""

  # The bot's username
  username: str
  # Information related to a bot's performance for a particular PerfType.
  perf: LeaderboardPerf
  # Information related to the bot's rank in the leaderboard row
  rank_info: RankInfo

  @classmethod
  def from_json(cls, json_str: str) -> "LeaderboardRow":
    """Create a LeaderboardRow from json."""
    json_dict = json.loads(json_str)
    return LeaderboardRow(
      json_dict.get("username", ""),
      LeaderboardPerf.from_json_dict(json_dict.get("perf", {})),
      RankInfo.from_json_dict(json_dict.get("rank_info", {})),
    )

  def to_json(self) -> str:
    """Convert the leaderboard row to json.

    Values will only be set if they are not equal to their default values.
    """
    return json.dumps(default_remover.to_dict_without_defaults(dataclasses.asdict(self)))
