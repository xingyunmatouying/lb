"""Dataclasses encapsulating updates to leaderboard rows."""

import abc
import dataclasses

from src.leaderboard.chrono.durations import TWO_WEEKS
from src.leaderboard.data.leaderboard_objects import BotPerf, LeaderboardRow, RankInfo


class LeaderboardUpdate(abc.ABC):
  """The information required to update a row in the leaderboard."""

  @abc.abstractmethod
  def get_name(self) -> str:
    """Return the bot's name."""
    ...

  @abc.abstractmethod
  def get_rating(self) -> int:
    """Return the bot's rating."""
    ...

  @abc.abstractmethod
  def get_rd(self) -> int:
    """Return the bot's rating deviation."""
    ...

  @abc.abstractmethod
  def is_eligible(self, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    ...

  @abc.abstractmethod
  def to_leaderboard_row(self, rank: int, current_time: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    ...

  @classmethod
  def create_update(cls, previous_row: LeaderboardRow | None, current_bot_perf: BotPerf | None) -> "LeaderboardUpdate":
    """Return the specific type of update based on the presence of previous_row and current_bot_perf.

    If both parameters are None, a ValueError will be raised.
    """
    if previous_row and current_bot_perf:
      return FullUpdate(previous_row, current_bot_perf)
    if previous_row and not current_bot_perf:
      return PreviousRowOnlyUpdate(previous_row)
    if current_bot_perf and not previous_row:
      return CurrentBotPerfOnlyUpdate(current_bot_perf)
    error_msg = "At least one of previous_row or current_bot_perf must be set."
    raise ValueError(error_msg)

  @classmethod
  def check_is_eligible(cls, prov: bool, last_played: int, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    played_in_last_two_weeks = current_time - last_played <= TWO_WEEKS
    return not prov and played_in_last_two_weeks


@dataclasses.dataclass(frozen=True)
class PreviousRowOnlyUpdate(LeaderboardUpdate):
  """Only the previous row was found.

  This happens when the bot has been seen previously but was not found now.
  """

  row: LeaderboardRow

  def get_name(self) -> str:
    """Return the bot's name."""
    return self.row.name

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.row.perf.rating

  def get_rd(self) -> int:
    """Return the bot's rating deviation."""
    return self.row.perf.rd

  def is_eligible(self, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    return LeaderboardUpdate.check_is_eligible(self.row.perf.prov, self.row.rank_info.last_played, current_time)

  def to_leaderboard_row(self, rank: int, current_time: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    del current_time
    delta_rank = self.row.rank_info.rank - rank
    delta_rating = 0
    delta_games = 0
    peak_rank = min(self.row.rank_info.rank, rank)
    peak_rating = self.row.rank_info.peak_rating
    last_played = self.row.rank_info.last_played
    rank_info = RankInfo(rank, delta_rank, delta_rating, delta_games, peak_rank, peak_rating, last_played)
    return LeaderboardRow(self.row.name, self.row.perf, rank_info)


@dataclasses.dataclass(frozen=True)
class CurrentBotPerfOnlyUpdate(LeaderboardUpdate):
  """Only the current perf was found.

  This happens when the bot is being seen for the first time.
  """

  bot_perf: BotPerf

  def get_name(self) -> str:
    """Return the bot's name."""
    return self.bot_perf.name

  def get_rating(self) -> int:
    """Return the bot's rating."""
    return self.bot_perf.perf.rating

  def get_rd(self) -> int:
    """Return the bot's rating deviation."""
    return self.bot_perf.perf.rd

  def is_eligible(self, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    return LeaderboardUpdate.check_is_eligible(self.bot_perf.perf.prov, current_time, current_time)

  def to_leaderboard_row(self, rank: int, current_time: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    delta_rank = 0
    delta_rating = 0
    delta_games = 0
    peak_rank = rank
    peak_rating = self.bot_perf.perf.rating
    # We don't actually know when the last played was in this case, so give the bot the benefit of the doubt.
    last_played = current_time
    rank_info = RankInfo(rank, delta_rank, delta_rating, delta_games, peak_rank, peak_rating, last_played)
    return LeaderboardRow(self.bot_perf.name, self.bot_perf.perf, rank_info)


@dataclasses.dataclass(frozen=True)
class FullUpdate(LeaderboardUpdate):
  """The bot is already on the leaderboard and we have new data."""

  previous_row: LeaderboardRow
  current_bot_perf: BotPerf

  def get_name(self) -> str:
    """Return the bot's name."""
    return self.current_bot_perf.name

  def get_rating(self) -> int:
    """Return the bot's rating."""
    # Use the current rating
    return self.current_bot_perf.perf.rating

  def get_rd(self) -> int:
    """Return the bot's rating deviation."""
    return self.current_bot_perf.perf.rd

  def get_delta_games_and_last_played(self, current_time: int) -> tuple[int, int]:
    """Return a pair of delta games and last played."""
    delta_games = self.current_bot_perf.perf.games - self.previous_row.perf.games
    last_played = current_time if delta_games else self.previous_row.rank_info.last_played
    return delta_games, last_played

  def is_eligible(self, current_time: int) -> bool:
    """Return whether the bot is eligible for the leaderboard."""
    _, last_played = self.get_delta_games_and_last_played(current_time)
    return LeaderboardUpdate.check_is_eligible(self.current_bot_perf.perf.prov, last_played, current_time)

  def to_leaderboard_row(self, rank: int, current_time: int) -> LeaderboardRow:
    """Convert the update information into a leaderboard row."""
    # Moving up in the leaderboard should count as a positive delta (3 -> 1 yields +2)
    delta_rank = self.previous_row.rank_info.rank - rank
    delta_rating = self.current_bot_perf.perf.rating - self.previous_row.perf.rating
    # Higher ranking, lower rank number
    peak_rank = min(self.previous_row.rank_info.rank, rank)
    peak_rating = max(self.previous_row.perf.rating, self.current_bot_perf.perf.rating)
    delta_games, last_played = self.get_delta_games_and_last_played(current_time)
    rank_info = RankInfo(rank, delta_rank, delta_rating, delta_games, peak_rank, peak_rating, last_played)
    return LeaderboardRow(self.current_bot_perf.name, self.current_bot_perf.perf, rank_info)
