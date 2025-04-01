"""Tests for data_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data import data_generator as data_generator_functions
from src.leaderboard.data.data_generator import DataGenerator
from src.leaderboard.data.leaderboard_row import BotInfo, BotProfile, LeaderboardPerf, LeaderboardRow
from src.leaderboard.data.leaderboard_update import CurrentBotInfoOnlyUpdate, LeaderboardUpdate
from src.leaderboard.fs import file_paths
from src.leaderboard.li.bot_user import PerfType
from tests.leaderboard.chrono.epoch_seconds import (
  DATE_2021_04_01,
  DATE_2022_04_01,
  DATE_2023_04_01,
  DATE_2024_04_01,
  DATE_2025_04_01,
)
from tests.leaderboard.fs.in_memory_file_system import InMemoryFileSystem
from tests.leaderboard.li.fake_lichess_client import FakeLichessClient


# Bullet leaderboard BotInfos
BOT_1_INFO_BULLET = BotInfo(
  BotProfile("Bot-1", "", "", DATE_2021_04_01, False, False), LeaderboardPerf(3000, 0, 0, 1000), DATE_2025_04_01
)
BOT_2_INFO_BULLET = BotInfo(
  BotProfile("Bot-2", "", "", DATE_2022_04_01, False, False), LeaderboardPerf(2900, 0, 0, 900), DATE_2025_04_01
)
BOT_3_INFO_BULLET = BotInfo(
  BotProfile("Bot-3", "", "", DATE_2023_04_01, False, False), LeaderboardPerf(2900, 0, 0, 800), DATE_2025_04_01
)
BOT_4_INFO_BULLET = BotInfo(
  BotProfile("Bot-4", "", "", DATE_2024_04_01, False, False), LeaderboardPerf(2800, 0, 0, 700), DATE_2025_04_01
)

# Blitz leaderboard BotInfos
BOT_1_INFO_BLITZ = BotInfo(
  BotProfile("Bot-1", "", "", DATE_2021_04_01, False, False), LeaderboardPerf(2500, 0, 0, 50), DATE_2025_04_01
)
BOT_2_INFO_BLITZ = BotInfo(
  BotProfile("Bot-2", "", "", DATE_2022_04_01, False, False), LeaderboardPerf(2600, 0, 0, 200), DATE_2025_04_01
)

# Bullet LeaderboardRows
BOT_1_ROW_BULLET = LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3001, False, True)
BOT_2_ROW_BULLET = LeaderboardRow(BOT_2_INFO_BULLET, 2, 1, -100, 1, 3000, False, True)

# Blitz LeaderboardRows
BOT_2_ROW_BLITZ = LeaderboardRow(BOT_1_INFO_BLITZ, 1, 1, 100, 1, 2600, False, True)
BOT_1_ROW_BLITZ = LeaderboardRow(BOT_2_INFO_BLITZ, 2, -1, -150, 1, 2650, False, True)

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
BOT_1_CURRENT_INFO_BULLET = BotInfo(
  BotProfile("Bot-1", "flair", "_earth", DATE_2024_04_01, True, False), LeaderboardPerf(2950, 42, -50, 1100), DATE_2025_04_01
)
BOT_2_CURRENT_INFO_BULLET = BotInfo(
  BotProfile("Bot-2", "", "", DATE_2022_04_01, False, False), LeaderboardPerf(3000, 0, 0, 1000), DATE_2025_04_01
)

BOT_1_CURRENT_INFO_BLITZ = BotInfo(
  BotProfile("Bot-1", "flair", "_earth", DATE_2024_04_01, True, False), LeaderboardPerf(2550, 0, 0, 100), DATE_2025_04_01
)
BOT_2_CURRENT_INFO_BLITZ = BotInfo(
  BotProfile("Bot-2", "", "", DATE_2022_04_01, False, False), LeaderboardPerf(2500, 0, 0, 300), DATE_2025_04_01
)


def remove_whitespace(whitespace_str: str) -> str:
  """Remove spaces and endlines for a string so it can be used as ndjson.

  For this to work the string cannot have spaces or endlines which are necessary.
  """
  return whitespace_str.replace(" ", "").replace("\n", "")


class TestDataGeneratorFunctions(unittest.TestCase):
  """Tests for data_generator functions."""

  def test_load_all_previous_rows_empty(self) -> None:
    file_system = InMemoryFileSystem()
    previous_rows_by_perf_type = data_generator_functions.load_all_previous_rows(file_system)
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertTrue(all(rows == [] for rows in previous_rows_by_perf_type.values()))

  def test_load_all_previous_rows(self) -> None:
    file_system = InMemoryFileSystem()
    bullet_leaderboard = [BOT_1_ROW_BULLET.to_json(), BOT_2_ROW_BULLET.to_json()]
    blitz_leaderboard = [BOT_2_ROW_BLITZ.to_json(), BOT_1_ROW_BLITZ.to_json()]
    file_system.save_file_lines(file_paths.data_path(PerfType.BULLET), bullet_leaderboard)
    file_system.save_file_lines(file_paths.data_path(PerfType.BLITZ), blitz_leaderboard)
    previous_rows_by_perf_type = data_generator_functions.load_all_previous_rows(file_system)
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertListEqual(previous_rows_by_perf_type[PerfType.BULLET], [BOT_1_ROW_BULLET, BOT_2_ROW_BULLET])
    self.assertListEqual(previous_rows_by_perf_type[PerfType.BLITZ], [BOT_2_ROW_BLITZ, BOT_1_ROW_BLITZ])

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
      BotProfile("Bot", "", "", DATE_2022_04_01, False, True), LeaderboardPerf(2500, 0, 0, 300), DATE_2025_04_01
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
      LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3000, True, True),
      LeaderboardRow(BOT_2_INFO_BULLET, 2, 0, 0, 2, 2900, True, True),
      LeaderboardRow(BOT_4_INFO_BULLET, 3, 0, 0, 3, 2800, True, True),
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
      LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3000, True, True),
      LeaderboardRow(BOT_2_INFO_BULLET, 2, 0, 0, 2, 2900, True, True),
      LeaderboardRow(BOT_3_INFO_BULLET, 2, 0, 0, 2, 2900, True, True),
      LeaderboardRow(BOT_4_INFO_BULLET, 4, 0, 0, 4, 2800, True, True),
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
      LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3000, True, True),
      LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3000, True, True),
      LeaderboardRow(BOT_1_INFO_BULLET, 1, 0, 0, 1, 3000, True, True),
      LeaderboardRow(BOT_4_INFO_BULLET, 4, 0, 0, 4, 2800, True, True),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)


class TestDataGenerator(unittest.TestCase):
  """Tests for DataGenerator."""

  def test_create_all_leaderboards(self) -> None:
    file_system = InMemoryFileSystem()
    bullet_ndjson = [BOT_1_ROW_BULLET.to_json(), BOT_2_ROW_BULLET.to_json()]
    file_system.save_file_lines(file_paths.data_path(PerfType.BULLET), bullet_ndjson)

    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("\n".join([remove_whitespace(BOT_1_CURRENT_JSON), remove_whitespace(BOT_2_CURRENT_JSON)]))

    time_provider = FixedTimeProvider(DATE_2025_04_01)

    data_generator = DataGenerator(file_system, lichess_client, time_provider)
    bullet_ranked_rows = data_generator.generate_leaderboard_data()[PerfType.BULLET]

    expected_ranked_rows = [
      LeaderboardRow(BOT_2_CURRENT_INFO_BULLET, 1, 1, 100, 1, 3000, False, True),
      LeaderboardRow(BOT_1_CURRENT_INFO_BULLET, 2, -1, -50, 1, 3000, False, True),
    ]
    self.assertListEqual(bullet_ranked_rows, expected_ranked_rows)
