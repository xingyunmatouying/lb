"""The main logic for generating the leaderboard data."""

import dataclasses
from collections import defaultdict

from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data.leaderboard_row import BotPerf, BotProfile, LeaderboardPerf, LeaderboardRow
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
  return {bot_profile.name: bot_profile for bot_profile in bot_profiles}


def load_leaderboard_rows(file_system: FileSystem) -> dict[PerfType, list[LeaderboardRow]]:
  """Load the previous leaderboard rows and return lists of leaderboard rows grouped by perf type."""
  previous_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]] = {}
  for perf_type in PerfType.all_except_unknown():
    ndjson = file_system.load_file_lines(file_paths.data_path(perf_type))
    previous_rows_by_perf_type[perf_type] = [LeaderboardRow.from_json(json_line) for json_line in ndjson]
  return previous_rows_by_perf_type


@dataclasses.dataclass(frozen=True)
class BotInfoResult:
  """The result of getting the information about the lichess bots currently online.

  This is a pair of a list of BotProfiles and lists of BotPerfs grouped by PerfType.
  """

  bot_profiles_by_name: dict[str, BotProfile]
  bot_perfs_by_perf_type: dict[PerfType, list[BotPerf]]


def get_online_bot_info(lichess_client: LichessClient) -> BotInfoResult:
  """Load all of the current online bots and return the information used to generate the leaderboard."""
  bot_profiles_by_name: dict[str, BotProfile] = {}
  bot_perfs_by_perf_type: dict[PerfType, list[BotPerf]] = defaultdict(list)
  for bot_json in lichess_client.get_online_bots().splitlines():
    bot_user = BotUser.from_json(bot_json)
    bot_profiles_by_name[bot_user.username] = BotProfile.from_bot_user(bot_user)
    for perf in bot_user.perfs:
      bot_perfs_by_perf_type[perf.perf_type].append(BotPerf(bot_user.username, LeaderboardPerf.from_perf(perf)))
  return BotInfoResult(bot_profiles_by_name, bot_perfs_by_perf_type)


def merge_bot_profiles(
  previous_profiles_by_name: dict[str, BotProfile], current_profiles_by_name: dict[str, BotProfile]
) -> dict[str, BotProfile]:
  """Merge and update the previous and current bot profiles."""
  merged_profiles_by_name: dict[str, BotProfile] = {}
  for name in previous_profiles_by_name.keys() | current_profiles_by_name.keys():
    previous_profile = previous_profiles_by_name.get(name)
    current_profile = current_profiles_by_name.get(name)
    if previous_profile and current_profile:
      merged_profiles_by_name[name] = current_profile.create_updated_copy_for_for_merge()
    if previous_profile and not current_profile:
      merged_profiles_by_name[name] = previous_profile
    if current_profile and not previous_profile:
      merged_profiles_by_name[name] = current_profile
  return merged_profiles_by_name


def create_updates(
  previous_rows: list[LeaderboardRow], current_bot_perfs: list[BotPerf], current_time: int
) -> list[LeaderboardUpdate]:
  """Group previous rows and current bot info by bot name and create updates."""
  previous_row_by_name: dict[str, LeaderboardRow] = {row.name: row for row in previous_rows}
  current_bot_perfs_by_name: dict[str, BotPerf] = {bot_perf.name: bot_perf for bot_perf in current_bot_perfs}
  return [
    LeaderboardUpdate.create_update(previous_row_by_name.get(name), current_bot_perfs_by_name.get(name), current_time)
    for name in previous_row_by_name.keys() | current_bot_perfs_by_name.keys()
  ]


def create_ranked_rows(
  updates: list[LeaderboardUpdate], bot_profiles_by_name: dict[str, BotProfile], current_time: int
) -> list[LeaderboardRow]:
  """Create the leaderboard rows for each perf type based on a list of updates."""
  new_rows: list[LeaderboardRow] = []
  # Primary sort: rating descending, Secondary sort: rd ascending, Tertiary sort: created time ascending
  sorted_update_list = sorted(
    updates, key=lambda update: (-update.get_rating(), update.get_rd(), bot_profiles_by_name[update.get_name()].created)
  )
  # The first in the list will be ranked #1
  rank = 0
  # Used for 1224 ranking (https://en.wikipedia.org/wiki/Ranking#Standard_competition_ranking_(%221224%22_ranking))
  same_rank_count = 0
  previous_rating = 0
  for update in sorted_update_list:
    # Rank equals zero signals that the bot should not be included on the leaderboard
    rank_to_set = 0
    bot_profile_eligible = bot_profiles_by_name[update.get_name()].is_eligible(current_time)
    if bot_profile_eligible and update.is_eligible(current_time):
      if update.get_rating() == previous_rating:
        same_rank_count += 1
      else:
        rank += same_rank_count
        rank += 1
        same_rank_count = 0
      rank_to_set = rank
    new_rows.append(update.to_leaderboard_row(rank_to_set))
    previous_rating = update.get_rating()
  return new_rows


@dataclasses.dataclass(frozen=True)
class LeaderboardDataResult:
  """The result of generating the leaderboard data.

  This is a pair of:
  - a dict from name to BotProfile
  - lists of LeaderboardRowLite grouped by PerfType
  """

  bot_profiles_by_name: dict[str, BotProfile]
  ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]]

  @classmethod
  def create_result(
    cls, bot_profiles_by_name: dict[str, BotProfile], ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]]
  ) -> "LeaderboardDataResult":
    """Create a data result with the data provided."""
    return LeaderboardDataResult(bot_profiles_by_name, ranked_rows_by_perf_type)

  def get_bot_profiles_sorted(self) -> dict[str, BotProfile]:
    """Return the bot profiles dict sorted by name."""
    return dict(sorted(self.bot_profiles_by_name.items(), key=lambda item: item[0].lower()))

  def get_ranked_rows_sorted(self) -> dict[PerfType, list[LeaderboardRow]]:
    """Return the ranked rows by perf type with the ranked rows sorted by name."""
    sorted_ranked_rows: dict[PerfType, list[LeaderboardRow]] = {}
    for perf_type, ranked_rows in self.ranked_rows_by_perf_type.items():
      sorted_ranked_rows[perf_type] = sorted(ranked_rows, key=lambda row: row.name.lower())
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

  def generate_leaderboard_data(self) -> LeaderboardDataResult:
    """Generate and save all leaderboard data."""
    # Load the existing leaderboard data
    bot_profiles_by_name = load_bot_profiles(self.file_system)
    previous_rows_by_perf_type = load_leaderboard_rows(self.file_system)
    # Get the current online bot info
    online_bot_info = get_online_bot_info(self.lichess_client)
    # Update the bot profiles
    updated_bot_profiles = merge_bot_profiles(bot_profiles_by_name, online_bot_info.bot_profiles_by_name)
    # Combine the data and create update objects for all of the leaderboards
    updates_by_perf_type = {
      perf_type: create_updates(
        previous_rows_by_perf_type.get(perf_type, []),
        online_bot_info.bot_perfs_by_perf_type.get(perf_type, []),
        self.time_provider.get_current_time(),
      )
      for perf_type in PerfType.all_except_unknown()
    }
    # Create and return the leaderboards with rank information
    ranked_rows_by_perf_type = {
      perf_type: create_ranked_rows(updates, updated_bot_profiles, self.time_provider.get_current_time())
      for perf_type, updates in updates_by_perf_type.items()
    }
    return LeaderboardDataResult.create_result(updated_bot_profiles, ranked_rows_by_perf_type)
