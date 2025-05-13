"""Dataclasses related rows in a leaderboard."""

import dataclasses
from typing import Any

from src.leaderboard.chrono.durations import TWO_WEEKS
from src.leaderboard.data import default_remover
from src.leaderboard.li.bot_user import BotUser, Perf


@dataclasses.dataclass(frozen=True)
class BotProfile:
  """Information related to the bot's profile.

  This is information that either never changes or does not change very often.
  """

  # The bot's name
  name: str
  # The bot's flair
  flair: str
  # The bot's country flag
  flag: str
  # The time the bot was created (seconds since epoch)
  created: int
  # The time the bot was last seen (seconds since epoch)
  last_seen: int
  # If the bot is a patron
  patron: bool
  # If the bot has violated the terms of service
  tos_violation: bool
  # Whether or not this is the bot's first time on the leaderboard
  new: bool
  # Whether or not the bot was online when the leaderboard was generated
  online: bool

  @classmethod
  def from_bot_user(cls, bot_user: BotUser) -> "BotProfile":
    """Create a BotProfile from a BotUser.

    The bot will be assumed to be new and to be online.
    """
    return BotProfile(
      bot_user.username,
      bot_user.flair,
      bot_user.flag,
      bot_user.created_at,
      bot_user.seen_at,
      bot_user.patron,
      bot_user.tos_violation,
      # Assume the bot is new - this simplifies updates
      True,
      # If we are creating a BotProfile from a BotUser then the bot is online
      True,
    )

  @classmethod
  def from_dict(cls, json_dict: dict[str, Any]) -> "BotProfile":
    """Create a BotProfile from a json dict.

    The bot will be assumed not to be new and to be offline.
    """
    return BotProfile(
      json_dict.get("name", ""),
      json_dict.get("flair", ""),
      json_dict.get("flag", ""),
      json_dict.get("created", 0),
      json_dict.get("last_seen", 0),
      json_dict.get("patron", False),
      json_dict.get("tos_violation", False),
      # If we are loading from json the bot is not new
      False,
      # Assume the bot is offline - this simplifies updates
      False,
    )

  def create_updated_copy_for_for_merge(self) -> "BotProfile":
    """Create an updated copy of the profile.

    The updated copy has new set to False and online set to True.
    """
    return BotProfile(
      self.name,
      self.flair,
      self.flag,
      self.created,
      self.last_seen,
      self.patron,
      self.tos_violation,
      False,
      True,
    )

  def is_eligible(self, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    seen_in_last_two_weeks = current_time - self.last_seen <= TWO_WEEKS
    return not self.tos_violation and seen_in_last_two_weeks

  def as_dict(self) -> dict[str, Any]:
    """Return the BotProfile represented as a dict.

    Values will only be set if they are not equal to their default values.
    """
    return default_remover.to_dict_without_defaults(dataclasses.asdict(self))


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
  # If the bot's rating is provisional
  prov: bool

  @classmethod
  def from_perf(cls, perf: Perf) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from a Perf."""
    return LeaderboardPerf(perf.rating, perf.rd, perf.prog, perf.games, perf.prov)

  @classmethod
  def from_dict(cls, json_dict: dict[str, Any]) -> "LeaderboardPerf":
    """Create a LeaderboardPerf from a json dict."""
    return LeaderboardPerf(
      json_dict.get("rating", 0),
      json_dict.get("rd", 0),
      json_dict.get("prog", 0),
      json_dict.get("games", 0),
      json_dict.get("prov", False),
    )


@dataclasses.dataclass(frozen=True)
class BotPerf:
  """A pair of bot name and LeaderboardPerf."""

  name: str
  perf: LeaderboardPerf


@dataclasses.dataclass(frozen=True)
class RankInfo:
  """Information related to the bot's rank in the leaderboard row."""

  # The bot's rank on the leaderboard
  # If rank is zero the bot should not be included on the leaderboard
  rank: int
  # How much the bot's rank has changed since last time
  delta_rank: int
  # How much the bot's rating has changed since last time
  delta_rating: int
  # How much the number of games played has changed since last time
  delta_games: int
  # The highest rank the bot has ever achieved on the leaderboard
  peak_rank: int
  # The maximum rating observed at any point when generating the leaderboard
  peak_rating: int
  # The time the bot was last detected having played a game
  last_played: int

  @classmethod
  def from_dict(cls, json_dict: dict[str, Any]) -> "RankInfo":
    """Create a RankInfo from a json dict."""
    return RankInfo(
      json_dict.get("rank", 0),
      json_dict.get("delta_rank", 0),
      json_dict.get("delta_rating", 0),
      json_dict.get("delta_games", 0),
      json_dict.get("peak_rank", 0),
      json_dict.get("peak_rating", 0),
      json_dict.get("last_played", 0),
    )


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """Data that is specific to a row on a particular leaderboard."""

  # The bot's name
  name: str
  # Information related to a bot's performance for a particular PerfType.
  perf: LeaderboardPerf
  # Information related to the bot's rank in the leaderboard row
  rank_info: RankInfo

  @classmethod
  def from_dict(cls, json_dict: dict[str, Any]) -> "LeaderboardRow":
    """Create a LeaderboardRow from a json dict."""
    return LeaderboardRow(
      json_dict.get("name", ""),
      LeaderboardPerf.from_dict(json_dict.get("perf", {})),
      RankInfo.from_dict(json_dict.get("rank_info", {})),
    )

  def as_dict(self) -> dict[str, Any]:
    """Return the LeaderboardRow represented as a dict.

    Values will only be set if they are not equal to their default values.
    """
    return default_remover.to_dict_without_defaults(dataclasses.asdict(self))
