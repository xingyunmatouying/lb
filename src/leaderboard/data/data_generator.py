"""The main logic for generating the leaderboards."""

from collections import defaultdict

from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data.leaderboard_data import LeaderboardPerf, LeaderboardRow, LeaderboardUpdate
from src.leaderboard.fs.file_system import FileSystem
from src.leaderboard.li.bot_user import BotUser, PerfType
from src.leaderboard.li.lichess_client import LichessClient


def get_leaderboard_data_file_name(perf_type: PerfType) -> str:
  """Return the data file name for a PerfType."""
  return f"leaderboard_data/{perf_type.to_string()}.ndjson"


def load_all_previous_rows(file_system: FileSystem) -> dict[PerfType, list[LeaderboardRow]]:
  """Load the previous leaderboards.

  Returns a lists of leaderboard rows grouped by perf type.
  """
  previous_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]] = {}
  for perf_type in PerfType.all_except_unknown():
    ndjson = file_system.load_file_lines(get_leaderboard_data_file_name(perf_type))
    previous_rows_by_perf_type[perf_type] = [LeaderboardRow.from_json(json_line) for json_line in ndjson]
  return previous_rows_by_perf_type


def get_all_current_perfs(lichess_client: LichessClient, time_provider: TimeProvider) -> dict[PerfType, list[LeaderboardPerf]]:
  """Load all of the current online bots.

  Returns lists of leaderboard perfs grouped by perf type.
  """
  current_date = time_provider.get_current_date_formatted()
  current_perfs_by_perf_type: dict[PerfType, list[LeaderboardPerf]] = defaultdict(list)
  for bot_json in lichess_client.get_online_bots().splitlines():
    bot_user = BotUser.from_json(bot_json)
    for perf in bot_user.perfs:
      # Don't include provisional ratings (this ends up being redundant if taking rd into account)
      if not perf.prov:
        current_perfs_by_perf_type[perf.perf_type].append(LeaderboardPerf.from_bot_user(bot_user, perf, current_date))
  return current_perfs_by_perf_type


def create_updates(previous_rows: list[LeaderboardRow], current_perfs: list[LeaderboardPerf]) -> list[LeaderboardUpdate]:
  """Group previous rows and current perfs by bot name and create updates."""
  previous_row_by_name: dict[str, LeaderboardRow] = {row.perf.username: row for row in previous_rows}
  current_perf_by_name: dict[str, LeaderboardPerf] = {perf.username: perf for perf in current_perfs}
  updates: list[LeaderboardUpdate] = []
  for name in previous_row_by_name.keys() | current_perf_by_name.keys():
    current_perf = current_perf_by_name.get(name)
    include_in_leaderboard = True
    if current_perf and current_perf.tos_violation:
      include_in_leaderboard = False
    if include_in_leaderboard:
      update = LeaderboardUpdate.create_update(previous_row_by_name.get(name), current_perf)
      updates.append(update)
  return updates


def create_ranked_rows(updates: list[LeaderboardUpdate]) -> list[LeaderboardRow]:
  """Create the leaderboard rows for each perf type based on a list of updates."""
  new_rows: list[LeaderboardRow] = []

  # Primary sort: by rating descending, Secondary sort: creation date ascending
  sorted_update_list = sorted(updates, key=lambda update: (-update.get_rating(), update.get_created_date()))

  # The first in the list will be ranked #1
  rank = 0

  # Used for 1224 ranking (https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking))
  same_rank_count = 0
  previous_rating = 0

  for update in sorted_update_list:
    if update.get_rating() == previous_rating:
      same_rank_count += 1
    else:
      rank += same_rank_count
      rank += 1
      same_rank_count = 0
    new_rows.append(update.to_leaderboard_row(rank))
    previous_rating = update.get_rating()

  return new_rows


class LeaderboardDataGenerator:
  """Generator for leaderboard data.

  The generator takes a file_system, a lichess_client, and a time_provider as parameters.
  """

  def __init__(self, file_system: FileSystem, lichess_client: LichessClient, time_provider: TimeProvider) -> None:
    """Initialize a new generator."""
    self.file_system: FileSystem = file_system
    self.lichess_client: LichessClient = lichess_client
    self.time_provider: TimeProvider = time_provider

  def generate_leaderboard_data(self) -> dict[PerfType, list[LeaderboardRow]]:
    """Generate and save all leaderboard data."""
    # Load the existing leaderboards
    previous_rows_by_perf_type = load_all_previous_rows(self.file_system)
    # Get the current online bot info
    current_perfs_by_perf_type = get_all_current_perfs(self.lichess_client, self.time_provider)
    # Combine the data and create update objects for all of the leaderboards
    updates_by_perf_type = {
      perf_type: create_updates(previous_rows_by_perf_type.get(perf_type, []), current_perfs_by_perf_type.get(perf_type, []))
      for perf_type in PerfType.all_except_unknown()
    }
    # Create and return the leaderboards with rank information
    return {perf_type: create_ranked_rows(updates) for perf_type, updates in updates_by_perf_type.items()}
