"""The main logic for generating the leaderboard data."""

import dataclasses
from collections import defaultdict

from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data.leaderboard_row import BotInfo, BotProfile, LeaderboardRow, LeaderboardRowLite
from src.leaderboard.data.leaderboard_update import LeaderboardUpdate
from src.leaderboard.fs import file_paths
from src.leaderboard.fs.file_system import FileSystem
from src.leaderboard.li.bot_user import BotUser
from src.leaderboard.li.lichess_client import LichessClient
from src.leaderboard.li.pert_type import PerfType


def load_bot_profiles(file_system: FileSystem) -> dict[str, BotProfile]:
  """Load the known bot profiles."""
  ndjson = file_system.load_file_lines(file_paths.bot_profiles_path())
  bot_profiles = [BotProfile.from_json(json_line) for json_line in ndjson]
  return {bot_profile.username: bot_profile for bot_profile in bot_profiles}


def load_all_previous_rows(
  file_system: FileSystem, bot_profiles_by_name: dict[str, BotProfile]
) -> dict[PerfType, list[LeaderboardRow]]:
  """Load the previous leaderboard data.

  Returns a lists of leaderboard rows grouped by perf type.
  """
  previous_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]] = {}
  for perf_type in PerfType.all_except_unknown():
    ndjson = file_system.load_file_lines(file_paths.data_path(perf_type))
    leaderboard_rows: list[LeaderboardRow] = []
    for json_line in ndjson:
      leaderboard_row_lite = LeaderboardRowLite.from_json(json_line)
      # It should always be the case that the profile exists
      leaderboard_rows.append(leaderboard_row_lite.to_leaderboard_row(bot_profiles_by_name[leaderboard_row_lite.username]))
    previous_rows_by_perf_type[perf_type] = leaderboard_rows
  return previous_rows_by_perf_type


def get_all_current_bot_infos(lichess_client: LichessClient, time_provider: TimeProvider) -> dict[PerfType, list[BotInfo]]:
  """Load all of the current online bots.

  Returns lists of BotInfo grouped by perf type.
  """
  current_time = time_provider.get_current_time()
  current_infos_by_perf_type: dict[PerfType, list[BotInfo]] = defaultdict(list)
  for bot_json in lichess_client.get_online_bots().splitlines():
    # TODO: no need to duplicate the BotUser for each perf type
    bot_user = BotUser.from_json(bot_json)
    for perf in bot_user.perfs:
      # Don't include provisional ratings (this ends up being redundant if taking rd into account)
      if not perf.prov:
        current_infos_by_perf_type[perf.perf_type].append(BotInfo.create_bot_info(bot_user, perf, current_time))
  return current_infos_by_perf_type


def create_updates(previous_rows: list[LeaderboardRow], current_bot_infos: list[BotInfo]) -> list[LeaderboardUpdate]:
  """Group previous rows and current bot info by bot name and create updates."""
  previous_row_by_name: dict[str, LeaderboardRow] = {row.bot_info.profile.username: row for row in previous_rows}
  current_bot_info_by_name: dict[str, BotInfo] = {bot_info.profile.username: bot_info for bot_info in current_bot_infos}
  updates: list[LeaderboardUpdate] = []
  for name in previous_row_by_name.keys() | current_bot_info_by_name.keys():
    current_bot_info = current_bot_info_by_name.get(name)
    include_in_leaderboard = True
    # Don't include bots with tos violations
    if current_bot_info and current_bot_info.profile.tos_violation:
      include_in_leaderboard = False
    if include_in_leaderboard:
      update = LeaderboardUpdate.create_update(previous_row_by_name.get(name), current_bot_info)
      updates.append(update)
  return updates


def create_ranked_rows(updates: list[LeaderboardUpdate]) -> list[LeaderboardRow]:
  """Create the leaderboard rows for each perf type based on a list of updates."""
  new_rows: list[LeaderboardRow] = []
  # Primary sort: by rating descending, Secondary sort: creation date ascending
  sorted_update_list = sorted(updates, key=lambda update: (-update.get_rating(), update.get_created_time()))
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


@dataclasses.dataclass(frozen=True)
class GenerateDataResult:
  """The result of generating the leaderboard data.

  This is a pair of:
  - a dict from name to BotProfile
  - lists of LeaderboardRowLite grouped by PerfType
  """

  bot_profiles_by_name: dict[str, BotProfile]
  ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRowLite]]

  @classmethod
  def create_result(
    cls, bot_profiles_by_name: dict[str, BotProfile], ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]]
  ) -> "GenerateDataResult":
    """Create a data result with the data provided."""
    # TODO need correct bot profiles - can get from ranked rows
    ranked_rows_lite_by_perf_type = {
      perf_type: [row.to_leaderboard_row_lite() for row in rows] for perf_type, rows in ranked_rows_by_perf_type.items()
    }
    return GenerateDataResult(bot_profiles_by_name, ranked_rows_lite_by_perf_type)

  def get_bot_profiles_sorted(self) -> dict[str, BotProfile]:
    """Return the bot profiles dict sorted by name."""
    return dict(sorted(self.bot_profiles_by_name.items(), key=lambda item: item[0].lower()))

  def get_ranked_rows_sorted(self) -> dict[PerfType, list[LeaderboardRowLite]]:
    """Return the ranked rows by perf type with the ranked rows sorted by name."""
    sorted_ranked_rows: dict[PerfType, list[LeaderboardRowLite]] = {}
    for perf_type, ranked_rows in self.ranked_rows_by_perf_type.items():
      sorted_ranked_rows[perf_type] = sorted(ranked_rows, key=lambda row: row.username.lower())
    return sorted_ranked_rows


class DataGenerator:
  """Generator of leaderboard data.

  The generator takes a file_system, a lichess_client, and a time_provider as parameters.
  """

  def __init__(self, file_system: FileSystem, lichess_client: LichessClient, time_provider: TimeProvider) -> None:
    """Initialize a new generator."""
    self.file_system: FileSystem = file_system
    self.lichess_client: LichessClient = lichess_client
    self.time_provider: TimeProvider = time_provider

  def generate_leaderboard_data(self) -> GenerateDataResult:
    """Generate and save all leaderboard data."""
    # Load the existing leaderboard data
    bot_profiles_by_name = load_bot_profiles(self.file_system)
    previous_rows_by_perf_type = load_all_previous_rows(self.file_system, bot_profiles_by_name)
    # Get the current online bot info
    current_infos_by_perf_type = get_all_current_bot_infos(self.lichess_client, self.time_provider)
    # Update the bot profiles
    for bot_infos in current_infos_by_perf_type.values():
      for bot_info in bot_infos:
        bot_profiles_by_name[bot_info.profile.username] = bot_info.profile
    # Combine the data and create update objects for all of the leaderboards
    updates_by_perf_type = {
      perf_type: create_updates(previous_rows_by_perf_type.get(perf_type, []), current_infos_by_perf_type.get(perf_type, []))
      for perf_type in PerfType.all_except_unknown()
    }
    # Create and return the leaderboards with rank information
    ranked_rows_by_perf_type = {perf_type: create_ranked_rows(updates) for perf_type, updates in updates_by_perf_type.items()}
    return GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
