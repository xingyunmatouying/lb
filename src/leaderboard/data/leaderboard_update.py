"""Dataclasses encapsulating updates to leaderboard rows."""

import abc
import dataclasses

from src.leaderboard.data.leaderboard_row import LeaderboardPerf, LeaderboardRow


class LeaderboardUpdate(abc.ABC):
  """The information required to update a row in the leaderboard."""

  @abc.abstractmethod
  def get_rating(self) -> int:
    """Return the bot's rating."""
    ...

  @abc.abstractmethod
  def get_created_date(self) -> str:
    """Return the date the bot was created."""
    ...

  @abc.abstractmethod
  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    ...

  @classmethod
  def create_update(cls, previous_row: LeaderboardRow | None, current_perf: LeaderboardPerf | None) -> "LeaderboardUpdate":
    """Return the specific type of update based on the presence of previous_row and current_perf.

    If both parameters are None, a ValueError will be raised.
    """
    if previous_row and not current_perf:
      return PreviousRowOnlyUpdate(previous_row)
    if current_perf and not previous_row:
      return CurrentPerfOnlyUpdate(current_perf)
    if previous_row and current_perf:
      return FullUpdate(previous_row, current_perf)
    raise ValueError("At least one of previous_row or current_perf must be set.")


@dataclasses.dataclass(frozen=True)
class PreviousRowOnlyUpdate(LeaderboardUpdate):
  """Only the previous row was found.

  This happens when the bot has been seen previously but was not found now.
  """

  row: LeaderboardRow

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.row.perf.rating

  def get_created_date(self) -> str:
    """Return the date the bot was created."""
    return self.row.perf.created_date

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    rank_delta = self.row.rank - rank
    rating_delta = 0
    peak_rank = min(self.row.rank, rank)
    peak_rating = self.row.peak_rating
    is_new = False
    is_online = False
    return LeaderboardRow(self.row.perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, is_new, is_online)


@dataclasses.dataclass(frozen=True)
class CurrentPerfOnlyUpdate(LeaderboardUpdate):
  """Only the current perf was found.

  This happens when the bot is being seen for the first time.
  """

  perf: LeaderboardPerf

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.perf.rating

  def get_created_date(self) -> str:
    """Return the date the bot was created."""
    return self.perf.created_date

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    rank_delta = 0
    rating_delta = 0
    peak_rank = rank
    peak_rating = self.perf.rating
    is_new = True
    is_online = True
    return LeaderboardRow(self.perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, is_new, is_online)


@dataclasses.dataclass(frozen=True)
class FullUpdate(LeaderboardUpdate):
  """The bot is already on the leaderboard and we have new data."""

  previous_row: LeaderboardRow
  current_perf: LeaderboardPerf

  def get_rating(self) -> int:
    """Return the bot's rating."""
    # Use the current rating
    return self.current_perf.rating

  def get_created_date(self) -> str:
    """Return the date the bot was created."""
    # The old and new created dates are expected to be the same
    return self.current_perf.created_date

  def to_leaderboard_row(self, rank: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    # Moving up in the leaderboard should count as a positive delta (3 -> 1 yields +2)
    rank_delta = self.previous_row.rank - rank
    rating_delta = self.current_perf.rating - self.previous_row.perf.rating
    # Higher ranking, lower rank number
    peak_rank = min(self.previous_row.rank, rank)
    peak_rating = max(self.previous_row.perf.rating, self.current_perf.rating)
    is_new = False
    is_online = True
    return LeaderboardRow(self.current_perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, is_new, is_online)
