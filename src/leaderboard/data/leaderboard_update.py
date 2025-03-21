"""Dataclasses encapsulating updates to leaderboard rows."""

import abc
import dataclasses

from src.leaderboard.data.leaderboard_row import BotInfo, LeaderboardRow


class LeaderboardUpdate(abc.ABC):
  """The information required to update a row in the leaderboard."""

  @abc.abstractmethod
  def get_rating(self) -> int:
    """Return the bot's rating."""
    ...

  @abc.abstractmethod
  def get_created_time(self) -> int:
    """Return the time the bot was created."""
    ...

  @abc.abstractmethod
  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    ...

  @classmethod
  def create_update(cls, previous_row: LeaderboardRow | None, current_bot_info: BotInfo | None) -> "LeaderboardUpdate":
    """Return the specific type of update based on the presence of previous_row and current_bot_info.

    If both parameters are None, a ValueError will be raised.
    """
    if previous_row and not current_bot_info:
      return PreviousRowOnlyUpdate(previous_row)
    if current_bot_info and not previous_row:
      return CurrentBotInfoOnlyUpdate(current_bot_info)
    if previous_row and current_bot_info:
      return FullUpdate(previous_row, current_bot_info)
    error_msg = "At least one of previous_row or current_bot_info must be set."
    raise ValueError(error_msg)


@dataclasses.dataclass(frozen=True)
class PreviousRowOnlyUpdate(LeaderboardUpdate):
  """Only the previous row was found.

  This happens when the bot has been seen previously but was not found now.
  """

  row: LeaderboardRow

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.row.bot_info.perf.rating

  def get_created_time(self) -> int:
    """Return the time the bot was created."""
    return self.row.bot_info.profile.created_time

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    delta_rank = self.row.rank - rank
    delta_rating = 0
    peak_rank = min(self.row.rank, rank)
    peak_rating = self.row.peak_rating
    is_new = False
    is_online = False
    return LeaderboardRow(self.row.bot_info, rank, delta_rank, delta_rating, peak_rank, peak_rating, is_new, is_online)


@dataclasses.dataclass(frozen=True)
class CurrentBotInfoOnlyUpdate(LeaderboardUpdate):
  """Only the current perf was found.

  This happens when the bot is being seen for the first time.
  """

  bot_info: BotInfo

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.bot_info.perf.rating

  def get_created_time(self) -> int:
    """Return the time the bot was created."""
    return self.bot_info.profile.created_time

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    delta_rank = 0
    delta_rating = 0
    peak_rank = rank
    peak_rating = self.bot_info.perf.rating
    is_new = True
    is_online = True
    return LeaderboardRow(self.bot_info, rank, delta_rank, delta_rating, peak_rank, peak_rating, is_new, is_online)


@dataclasses.dataclass(frozen=True)
class FullUpdate(LeaderboardUpdate):
  """The bot is already on the leaderboard and we have new data."""

  previous_row: LeaderboardRow
  current_bot_info: BotInfo

  def get_rating(self) -> int:
    """Return the bot's rating."""
    # Use the current rating
    return self.current_bot_info.perf.rating

  def get_created_time(self) -> int:
    """Return the time the bot was created."""
    # The old and new created times are expected to be the same
    return self.current_bot_info.profile.created_time

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    # Moving up in the leaderboard should count as a positive delta (3 -> 1 yields +2)
    delta_rank = self.previous_row.rank - rank
    delta_rating = self.current_bot_info.perf.rating - self.previous_row.bot_info.perf.rating
    # Higher ranking, lower rank number
    peak_rank = min(self.previous_row.rank, rank)
    peak_rating = max(self.previous_row.bot_info.perf.rating, self.current_bot_info.perf.rating)
    is_new = False
    is_online = True
    return LeaderboardRow(self.current_bot_info, rank, delta_rank, delta_rating, peak_rank, peak_rating, is_new, is_online)
