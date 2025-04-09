"""Tests for data_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data import data_generator as data_generator_functions
from src.leaderboard.data.data_generator import DataGenerator
from src.leaderboard.data.leaderboard_row import (
  BotInfo,
  BotProfile,
  LeaderboardPerf,
  LeaderboardRow,
  LeaderboardRowLite,
  RankInfo,
)
from src.leaderboard.data.leaderboard_update import CurrentBotInfoOnlyUpdate, LeaderboardUpdate
from src.leaderboard.fs import file_paths
from src.leaderboard.li.pert_type import PerfType
from tests.leaderboard.chrono.epoch_seconds import (
  DATE_2021_04_01,
  DATE_2022_04_01,
  DATE_2023_04_01,
  DATE_2024_04_01,
  DATE_2025_04_01,
)
from tests.leaderboard.fs.in_memory_file_system import InMemoryFileSystem
from tests.leaderboard.li.fake_lichess_client import FakeLichessClient


BOT_1_PROFILE = BotProfile("Bot-1", "", "", DATE_2021_04_01, DATE_2025_04_01, False, False)
BOT_2_PROFILE = BotProfile("Bot-2", "", "", DATE_2022_04_01, DATE_2025_04_01, False, False)

# Bullet leaderboard data
BOT_1_PERF_BULLET = LeaderboardPerf(3000, 0, 0, 1000)
BOT_2_PERF_BULLET = LeaderboardPerf(2900, 0, 0, 900)
BOT_3_PERF_BULLET = LeaderboardPerf(2900, 0, 0, 800)
BOT_4_PERF_BULLET = LeaderboardPerf(2800, 0, 0, 700)

BOT_1_INFO_BULLET = BotInfo(BOT_1_PROFILE, BOT_1_PERF_BULLET)
BOT_2_INFO_BULLET = BotInfo(BOT_2_PROFILE, BOT_2_PERF_BULLET)
BOT_3_INFO_BULLET = BotInfo(BotProfile("Bot-3", "", "", DATE_2023_04_01, DATE_2025_04_01, False, False), BOT_3_PERF_BULLET)
BOT_4_INFO_BULLET = BotInfo(BotProfile("Bot-4", "", "", DATE_2024_04_01, DATE_2025_04_01, False, False), BOT_4_PERF_BULLET)

BOT_1_ROW_BULLET = LeaderboardRowLite("Bot-1", BOT_1_PERF_BULLET, RankInfo(1, 0, 0, 1, 3001, False, True))
BOT_2_ROW_BULLET = LeaderboardRowLite("Bot-2", BOT_2_PERF_BULLET, RankInfo(2, 1, -100, 1, 3000, False, True))

# Blitz leaderboard data
BOT_1_PERF_BLITZ = LeaderboardPerf(2500, 0, 0, 50)
BOT_2_PERF_BLITZ = LeaderboardPerf(2600, 0, 0, 200)

BOT_1_INFO_BLITZ = BotInfo(BOT_1_PROFILE, BOT_1_PERF_BLITZ)
BOT_2_INFO_BLITZ = BotInfo(BOT_2_PROFILE, BOT_2_PERF_BLITZ)

BOT_2_ROW_BLITZ = LeaderboardRowLite("Bot-1", BOT_1_PERF_BLITZ, RankInfo(1, 1, 100, 1, 2600, False, True))
BOT_1_ROW_BLITZ = LeaderboardRowLite("Bot-2", BOT_2_PERF_BLITZ, RankInfo(2, -1, -150, 1, 2650, False, True))

# Response for get online bots
BOT_1_CURRENT_JSON = """
{
  "username": "Bot-1",
  "flair": "flair",
  "profile": {
    "flag": "_earth"
  },
  "createdAt": 1712000000000,
  "patron": true,
  "perfs": {
    "bullet": {
        "games": 1100,
        "rating": 2950,
        "rd": 42,
        "prog": -50
    },
    "blitz": {
        "games": 100,
        "rating": 2550
    }
  }
}
"""
BOT_2_CURRENT_JSON = """
{
  "username": "Bot-2",
  "createdAt": 1648800000000,
  "perfs": {
    "bullet": {
        "games": 1000,
        "rating": 3000
    },
    "blitz": {
        "games": 300,
        "rating": 2500
    }
  }
}
"""

# Leaderboard Perfs matching the above json
BOT_1_CURRENT_PROFILE = BotProfile("Bot-1", "flair", "_earth", DATE_2024_04_01, DATE_2025_04_01, True, False)
BOT_2_CURRENT_PROFILE = BotProfile("Bot-2", "", "", DATE_2022_04_01, DATE_2025_04_01, False, False)

BOT_1_CURRENT_PERF_BULLET = LeaderboardPerf(2950, 42, -50, 1100)
BOT_2_CURRENT_PERF_BULLET = LeaderboardPerf(3000, 0, 0, 1000)

BOT_1_CURRENT_INFO_BULLET = BotInfo(BOT_1_CURRENT_PROFILE, BOT_1_CURRENT_PERF_BULLET)
BOT_2_CURRENT_INFO_BULLET = BotInfo(BOT_2_CURRENT_PROFILE, BOT_2_CURRENT_PERF_BULLET)

BOT_1_CURRENT_INFO_BLITZ = BotInfo(BOT_1_CURRENT_PROFILE, LeaderboardPerf(2550, 0, 0, 100))
BOT_2_CURRENT_INFO_BLITZ = BotInfo(BOT_2_CURRENT_PROFILE, LeaderboardPerf(2500, 0, 0, 300))


def remove_whitespace(whitespace_str: str) -> str:
  """Remove spaces and endlines for a string so it can be used as ndjson.

  For this to work the string cannot have spaces or endlines which are necessary.
  """
  return whitespace_str.replace(" ", "").replace("\n", "")


class TestDataGeneratorFunctions(unittest.TestCase):
  """Tests for data_generator functions."""

  def test_load_all_previous_rows_empty(self) -> None:
    file_system = InMemoryFileSystem()
    previous_rows_by_perf_type = data_generator_functions.load_all_previous_rows(file_system, {})
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertTrue(all(rows == [] for rows in previous_rows_by_perf_type.values()))

  def test_load_all_previous_rows(self) -> None:
    file_system = InMemoryFileSystem()
    bullet_leaderboard = [BOT_1_ROW_BULLET.to_json(), BOT_2_ROW_BULLET.to_json()]
    blitz_leaderboard = [BOT_2_ROW_BLITZ.to_json(), BOT_1_ROW_BLITZ.to_json()]
    file_system.save_file_lines(file_paths.data_path(PerfType.BULLET), bullet_leaderboard)
    file_system.save_file_lines(file_paths.data_path(PerfType.BLITZ), blitz_leaderboard)
    bot_profiles_by_name = {"Bot-1": BOT_1_PROFILE, "Bot-2": BOT_2_PROFILE}
    previous_rows_by_perf_type = data_generator_functions.load_all_previous_rows(file_system, bot_profiles_by_name)
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertListEqual(
      previous_rows_by_perf_type[PerfType.BULLET],
      [BOT_1_ROW_BULLET.to_leaderboard_row(BOT_1_PROFILE), BOT_2_ROW_BULLET.to_leaderboard_row(BOT_2_PROFILE)],
    )
    self.assertListEqual(
      previous_rows_by_perf_type[PerfType.BLITZ],
      [BOT_2_ROW_BLITZ.to_leaderboard_row(BOT_1_PROFILE), BOT_1_ROW_BLITZ.to_leaderboard_row(BOT_2_PROFILE)],
    )

  def test_get_all_current_bot_infos(self) -> None:
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("\n".join([remove_whitespace(BOT_1_CURRENT_JSON), remove_whitespace(BOT_2_CURRENT_JSON)]))
    time_provider = FixedTimeProvider(DATE_2025_04_01)
    current_infos_by_perf_type = data_generator_functions.get_all_current_bot_infos(lichess_client, time_provider)
    self.assertEqual(len(current_infos_by_perf_type), 2)
    self.assertListEqual(current_infos_by_perf_type[PerfType.BULLET], [BOT_1_CURRENT_INFO_BULLET, BOT_2_CURRENT_INFO_BULLET])
    self.assertListEqual(current_infos_by_perf_type[PerfType.BLITZ], [BOT_1_CURRENT_INFO_BLITZ, BOT_2_CURRENT_INFO_BLITZ])

  def test_get_all_current_bot_infos_no_provisional(self) -> None:
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("""{"username":"Bot","perfs":{"bullet":{"rating":3000,"prov":true}}}\n""")
    current_infos_by_perf_type = data_generator_functions.get_all_current_bot_infos(lichess_client, FixedTimeProvider(0))
    self.assertDictEqual(current_infos_by_perf_type, {})

  def test_create_updates(self) -> None:
    updates = data_generator_functions.create_updates([], [BOT_1_CURRENT_INFO_BULLET, BOT_2_CURRENT_INFO_BULLET])
    expected_updates = [
      CurrentBotInfoOnlyUpdate(BOT_1_CURRENT_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_2_CURRENT_INFO_BULLET),
    ]
    self.assertCountEqual(updates, expected_updates)

  def test_create_updates_no_tos_violation(self) -> None:
    bot_with_tos_violation = BotInfo(
      BotProfile("Bot", "", "", DATE_2022_04_01, DATE_2025_04_01, False, True), LeaderboardPerf(2500, 0, 0, 300)
    )
    updates = data_generator_functions.create_updates([], [bot_with_tos_violation])
    self.assertCountEqual(updates, [])

  def test_create_ranked_rows(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentBotInfoOnlyUpdate(BOT_2_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_1_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_4_INFO_BULLET),
    ]
    leaderboard_rows = data_generator_functions.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_INFO_BULLET, RankInfo(1, 0, 0, 1, 3000, True, True)),
      LeaderboardRow(BOT_2_INFO_BULLET, RankInfo(2, 0, 0, 2, 2900, True, True)),
      LeaderboardRow(BOT_4_INFO_BULLET, RankInfo(3, 0, 0, 3, 2800, True, True)),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)

  def test_create_leaderboard_rows_with_tied_ratings(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentBotInfoOnlyUpdate(BOT_2_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_1_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_4_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_3_INFO_BULLET),
    ]
    leaderboard_rows = data_generator_functions.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_INFO_BULLET, RankInfo(1, 0, 0, 1, 3000, True, True)),
      LeaderboardRow(BOT_2_INFO_BULLET, RankInfo(2, 0, 0, 2, 2900, True, True)),
      LeaderboardRow(BOT_3_INFO_BULLET, RankInfo(2, 0, 0, 2, 2900, True, True)),
      LeaderboardRow(BOT_4_INFO_BULLET, RankInfo(4, 0, 0, 4, 2800, True, True)),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)

  def test_create_leaderboard_rows_with_three_way_tie(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentBotInfoOnlyUpdate(BOT_1_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_4_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_1_INFO_BULLET),
      CurrentBotInfoOnlyUpdate(BOT_1_INFO_BULLET),
    ]
    leaderboard_rows = data_generator_functions.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_INFO_BULLET, RankInfo(1, 0, 0, 1, 3000, True, True)),
      LeaderboardRow(BOT_1_INFO_BULLET, RankInfo(1, 0, 0, 1, 3000, True, True)),
      LeaderboardRow(BOT_1_INFO_BULLET, RankInfo(1, 0, 0, 1, 3000, True, True)),
      LeaderboardRow(BOT_4_INFO_BULLET, RankInfo(4, 0, 0, 4, 2800, True, True)),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)


class TestDataGenerator(unittest.TestCase):
  """Tests for DataGenerator."""

  def test_create_all_leaderboards(self) -> None:
    file_system = InMemoryFileSystem()

    bullet_ndjson = [BOT_1_ROW_BULLET.to_json(), BOT_2_ROW_BULLET.to_json()]
    file_system.save_file_lines(file_paths.data_path(PerfType.BULLET), bullet_ndjson)

    bot_profiles_json = [BOT_1_PROFILE.to_json(), BOT_2_PROFILE.to_json()]
    file_system.save_file_lines(file_paths.bot_profiles_path(), bot_profiles_json)

    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("\n".join([remove_whitespace(BOT_1_CURRENT_JSON), remove_whitespace(BOT_2_CURRENT_JSON)]))

    time_provider = FixedTimeProvider(DATE_2025_04_01)

    data_generator = DataGenerator(file_system, lichess_client, time_provider)
    generate_data_result = data_generator.generate_leaderboard_data()

    expected_ranked_rows = [
      LeaderboardRowLite("Bot-1", BOT_1_CURRENT_PERF_BULLET, RankInfo(2, -1, -50, 1, 3000, False, True)),
      LeaderboardRowLite("Bot-2", BOT_2_CURRENT_PERF_BULLET, RankInfo(1, 1, 100, 1, 3000, False, True)),
    ]
    self.assertListEqual(generate_data_result.get_ranked_rows_sorted()[PerfType.BULLET], expected_ranked_rows)

    expected_bot_profiles = {"Bot-1": BOT_1_CURRENT_PROFILE, "Bot-2": BOT_2_CURRENT_PROFILE}
    self.assertEqual(generate_data_result.get_bot_profiles_sorted(), expected_bot_profiles)
