"""Leaderboard-related dataclasses."""

import abc
import dataclasses

from src.generate.lichess_bot_user import BotUser, Perf


@dataclasses.dataclass(frozen=True)
class LeaderboardPerf:
  """A bots performance for a known PerfType.

  The performance type is not stored within this object itself.

  This also contains some additional information about the bot.
  """

  # The bot's username
  username: str

  # The country flag
  flag: str

  # The bot's rating for a particular PerfType
  rating: int

  # The number of games the bot has played for this PerfType
  games: int

  # The date the bot was created (YYYY-MM-DD)
  created_date: str

  # The date the bot was last seen (YYYY-MM-DD)
  last_seen_date: str

  @classmethod
  def from_bot_user(cls, bot_user: BotUser, perf: Perf, last_seen_date: str) -> "LeaderboardPerf":
    """Create a leaderboard perf from a bot user and a perf."""
    return LeaderboardPerf(bot_user.username, bot_user.flag, perf.rating, perf.games, bot_user.created_date, last_seen_date)


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

  # Whether or not this is the bots first time on the leaderboard.
  is_new: bool

  @classmethod
  def from_psv(cls, psv_string: str) -> "LeaderboardRow":
    """Create a LeaderboardRow based on pipe separated values."""
    values = psv_string.split("|")

    username = values[0]
    flag = values[1]
    rating = int(values[2])
    games = int(values[3])
    created_date = values[4]
    last_seen_date = values[5]
    perf = LeaderboardPerf(username, flag, rating, games, created_date, last_seen_date)

    rank = int(values[6])
    rank_delta = int(values[7])
    rating_delta = int(values[8])
    peak_rank = int(values[9])
    peak_rating = int(values[10])
    is_new = values[11] == "True"

    return LeaderboardRow(perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, is_new)

  def to_psv(self) -> str:
    """Convert the bot in to a string of pipe separated values."""
    values: list[str] = [
      self.perf.username,
      self.perf.flag,
      str(self.perf.rating),
      str(self.perf.games),
      self.perf.created_date,
      self.perf.last_seen_date,
      str(self.rank),
      str(self.rank_delta),
      str(self.rating_delta),
      str(self.peak_rank),
      str(self.peak_rating),
      str(self.is_new),
    ]
    return "|".join(values)


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
    return LeaderboardRow(self.row.perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, False)


@dataclasses.dataclass(frozen=True)
class CurrentPerfOnlyUpdate(LeaderboardUpdate):
  """Only the previous row was found.

  This happens when the bot has been seen previously but was not found now.
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
    return LeaderboardRow(self.perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, True)


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
    return LeaderboardRow(self.current_perf, rank, rank_delta, rating_delta, peak_rank, peak_rating, False)
