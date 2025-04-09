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

  @classmethod
  def from_bot_user(cls, bot_user: BotUser, last_seen_time: int) -> "BotProfile":
    """Create a BotProfile from a BotUser."""
    return BotProfile(
      bot_user.username,
      bot_user.flair,
      bot_user.flag,
      bot_user.created_at,
      last_seen_time,
      bot_user.patron,
      bot_user.tos_violation,
    )

  @classmethod
  def from_json(cls, json_str: str) -> "BotProfile":
    """Create a BotProfile from json."""
    return BotProfile.from_json_dict(json.loads(json_str))

  @classmethod
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "BotProfile":
    """Create a BotProfile from a json dict."""
    return BotProfile(
      json_dict.get("username", ""),
      json_dict.get("flair", ""),
      json_dict.get("flag", ""),
      json_dict.get("created_time", 0),
      json_dict.get("last_seen_time", 0),
      json_dict.get("patron", False),
      json_dict.get("tos_violation", False),
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
class BotInfo:
  """Information about the bot which may appear on the leaderboard.

  This class is useful for translating what is returned by lichess into a leaderboard row.
  """

  # Information related to the bot's profile.
  profile: BotProfile
  # Information related to a bot's performance for a particular PerfType.
  perf: LeaderboardPerf

  @classmethod
  def create_bot_info(cls, bot_user: BotUser, perf: Perf, last_seen_time: int) -> "BotInfo":
    """Create a BotInfo from information returned by the lichess API."""
    return BotInfo(BotProfile.from_bot_user(bot_user, last_seen_time), LeaderboardPerf.from_perf(perf))

  @classmethod
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "BotInfo":
    """Create a BotInfo from a json dict."""
    return BotInfo(
      BotProfile.from_json_dict(json_dict.get("profile", {})), LeaderboardPerf.from_json_dict(json_dict.get("perf", {}))
    )


@dataclasses.dataclass(frozen=True)
class RankInfo:
  """Information related to the bot's rank in the leaderboard row."""

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
  def from_json_dict(cls, json_dict: dict[str, Any]) -> "RankInfo":
    """Create a RankInfo from a json dict."""
    return RankInfo(
      json_dict.get("rank", 0),
      json_dict.get("delta_rank", 0),
      json_dict.get("delta_rating", 0),
      json_dict.get("peak_rank", 0),
      json_dict.get("peak_rating", 0),
      json_dict.get("is_new", False),
      json_dict.get("is_online", False),
    )


@dataclasses.dataclass(frozen=True)
class LeaderboardRow:
  """A row in the leaderboard: rank, name, rating, etc..."""

  # Information about the bot returned by the lichess API
  bot_info: BotInfo
  # Information related to the bot's rank in the leaderboard row
  rank_info: RankInfo

  def to_leaderboard_row_lite(self) -> "LeaderboardRowLite":
    """Convert to a LeaderboardRowLite."""
    return LeaderboardRowLite(self.bot_info.profile.username, self.bot_info.perf, self.rank_info)


@dataclasses.dataclass(frozen=True)
class LeaderboardRowLite:
  """Data that is specific to a row on a particular leaderboard."""

  # The bot's username
  username: str
  # Information related to a bot's performance for a particular PerfType.
  perf: LeaderboardPerf
  # Information related to the bot's rank in the leaderboard row
  rank_info: RankInfo

  @classmethod
  def from_json(cls, json_str: str) -> "LeaderboardRowLite":
    """Create a LeaderboardRow from json."""
    json_dict = json.loads(json_str)
    return LeaderboardRowLite(
      json_dict.get("username", ""),
      LeaderboardPerf.from_json_dict(json_dict.get("perf", {})),
      RankInfo.from_json_dict(json_dict.get("rank_info", {})),
    )

  def to_leaderboard_row(self, bot_profile: BotProfile) -> LeaderboardRow:
    """With the addition of a BotProfile, Convert to a LeaderboardRow."""
    return LeaderboardRow(BotInfo(bot_profile, self.perf), self.rank_info)

  def to_json(self) -> str:
    """Convert the leaderboard row to json.

    Values will only be set if they are not equal to their default values.
    """
    return json.dumps(default_remover.to_dict_without_defaults(dataclasses.asdict(self)))
