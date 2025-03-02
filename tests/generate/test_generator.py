"""Tests for generator.py."""

import unittest

from src.generate import generator
from src.generate.generator import LeaderboardGenerator
from src.generate.leaderboard_data import CurrentPerfOnlyUpdate, LeaderboardPerf, LeaderboardRow, LeaderboardUpdate
from src.generate.lichess_bot_user import PerfType

from generate.fake_date_provider import FakeDateProvider
from generate.fake_lichess_client import FakeLichessClient
from generate.in_memory_file_system import InMemoryFileSystem


# Bullet leaderboard perfs
BOT_1_PERF_BULLET = LeaderboardPerf("Bot-1", "", "", 3000, 0, 0, 1000, "2021-04-01", "2025-04-01", False, False)
BOT_2_PERF_BULLET = LeaderboardPerf("Bot-2", "", "", 2900, 0, 0, 900, "2022-04-01", "2025-04-01", False, False)
BOT_3_PERF_BULLET = LeaderboardPerf("Bot-3", "", "", 2900, 0, 0, 800, "2023-04-01", "2025-04-01", False, False)
BOT_4_PERF_BULLET = LeaderboardPerf("Bot-4", "", "", 2800, 0, 0, 700, "2024-04-01", "2025-04-01", False, False)

# Blitz leaderboard perfs
BOT_1_PERF_BLITZ = LeaderboardPerf("Bot-1", "", "", 2500, 0, 0, 50, "2021-04-01", "2025-04-01", False, False)
BOT_2_PERF_BLITZ = LeaderboardPerf("Bot-2", "", "", 2600, 0, 0, 200, "2022-04-01", "2025-04-01", False, False)

# Bullet leaderboard rows
BOT_1_ROW_BULLET = LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3001, False)
BOT_2_ROW_BULLET = LeaderboardRow(BOT_2_PERF_BULLET, 2, 1, -100, 1, 3000, False)

# Blitz leaderboard rows
BOT_2_ROW_BLITZ = LeaderboardRow(BOT_1_PERF_BLITZ, 1, 1, 100, 1, 2600, False)
BOT_1_ROW_BLITZ = LeaderboardRow(BOT_2_PERF_BLITZ, 2, -1, -150, 1, 2650, False)

# Response for get online bots
BOT_1_CURRENT_JSON = """
{
  "username": "Bot-1",
  "flair": "flair",
  "profile": {
    "flag": "_earth"
  },
  "createdAt": 1711929600000,
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
  "createdAt": 1648771200000,
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
BOT_1_CURRENT_PERF_BULLET = LeaderboardPerf(
  "Bot-1", "flair", "_earth", 2950, 42, -50, 1100, "2024-04-01", "2025-04-01", True, False
)
BOT_2_CURRENT_PERF_BULLET = LeaderboardPerf("Bot-2", "", "", 3000, 0, 0, 1000, "2022-04-01", "2025-04-01", False, False)

BOT_1_CURRENT_PERF_BLITZ = LeaderboardPerf(
  "Bot-1", "flair", "_earth", 2550, 0, 0, 100, "2024-04-01", "2025-04-01", True, False
)
BOT_2_CURRENT_PERF_BLITZ = LeaderboardPerf("Bot-2", "", "", 2500, 0, 0, 300, "2022-04-01", "2025-04-01", False, False)


def remove_whitespace(whitespace_str: str) -> str:
  """Remove spaces and endlines for a string so it can be used as ndjson.

  For this to work the string cannot have spaces or endlines which are necessary.
  """
  return whitespace_str.replace(" ", "").replace("\n", "")


class TestGenerator(unittest.TestCase):
  """Tests for generator functions."""

  def test_get_psv_file_name(self) -> None:
    self.assertEqual(generator.get_psv_file_name(PerfType.BLITZ), "leaderboard_data/blitz.psv")

  def test_load_all_previous_rows_empty(self) -> None:
    file_system = InMemoryFileSystem()
    previous_rows_by_perf_type = generator.load_all_previous_rows(file_system)
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertTrue(all(rows == [] for rows in previous_rows_by_perf_type.values()))

  def test_load_all_previous_rows(self) -> None:
    file_system = InMemoryFileSystem()
    bullet_leaderboard = [BOT_1_ROW_BULLET.to_psv(), BOT_2_ROW_BULLET.to_psv()]
    blitz_leaderboard = [BOT_2_ROW_BLITZ.to_psv(), BOT_1_ROW_BLITZ.to_psv()]
    file_system.save_file_lines(generator.get_psv_file_name(PerfType.BULLET), bullet_leaderboard)
    file_system.save_file_lines(generator.get_psv_file_name(PerfType.BLITZ), blitz_leaderboard)
    previous_rows_by_perf_type = generator.load_all_previous_rows(file_system)
    self.assertEqual(len(previous_rows_by_perf_type), 13)
    self.assertListEqual(previous_rows_by_perf_type[PerfType.BULLET], [BOT_1_ROW_BULLET, BOT_2_ROW_BULLET])
    self.assertListEqual(previous_rows_by_perf_type[PerfType.BLITZ], [BOT_2_ROW_BLITZ, BOT_1_ROW_BLITZ])

  def test_get_all_current_perfs(self) -> None:
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("\n".join([remove_whitespace(BOT_1_CURRENT_JSON), remove_whitespace(BOT_2_CURRENT_JSON)]))
    date_provider = FakeDateProvider()
    date_provider.set_current_date("2025-04-01")
    current_perfs_by_perf_type = generator.get_all_current_perfs(lichess_client, date_provider)
    self.assertEqual(len(current_perfs_by_perf_type), 2)
    self.assertListEqual(current_perfs_by_perf_type[PerfType.BULLET], [BOT_1_CURRENT_PERF_BULLET, BOT_2_CURRENT_PERF_BULLET])
    self.assertListEqual(current_perfs_by_perf_type[PerfType.BLITZ], [BOT_1_CURRENT_PERF_BLITZ, BOT_2_CURRENT_PERF_BLITZ])

  def test_get_all_current_perfs_no_provisional(self) -> None:
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("""{"username":"Bot","perfs":{"bullet":{"rating":3000,"prov":true}}}\n""")
    current_perfs_by_perf_type = generator.get_all_current_perfs(lichess_client, FakeDateProvider())
    self.assertDictEqual(current_perfs_by_perf_type, {})

  def test_create_updates(self) -> None:
    updates = generator.create_updates([], [BOT_1_CURRENT_PERF_BULLET, BOT_2_CURRENT_PERF_BULLET])
    expected_updates = [CurrentPerfOnlyUpdate(BOT_1_CURRENT_PERF_BULLET), CurrentPerfOnlyUpdate(BOT_2_CURRENT_PERF_BULLET)]
    self.assertCountEqual(updates, expected_updates)

  def test_create_ranked_rows(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentPerfOnlyUpdate(BOT_2_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_1_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_4_PERF_BULLET),
    ]
    leaderboard_rows = generator.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3000, True),
      LeaderboardRow(BOT_2_PERF_BULLET, 2, 0, 0, 2, 2900, True),
      LeaderboardRow(BOT_4_PERF_BULLET, 3, 0, 0, 3, 2800, True),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)

  def test_create_leaderboard_rows_with_tied_ratings(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentPerfOnlyUpdate(BOT_2_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_1_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_4_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_3_PERF_BULLET),
    ]
    leaderboard_rows = generator.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3000, True),
      LeaderboardRow(BOT_2_PERF_BULLET, 2, 0, 0, 2, 2900, True),
      LeaderboardRow(BOT_3_PERF_BULLET, 2, 0, 0, 2, 2900, True),
      LeaderboardRow(BOT_4_PERF_BULLET, 4, 0, 0, 4, 2800, True),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)

  def test_create_leaderboard_rows_with_three_way_tie(self) -> None:
    updates: list[LeaderboardUpdate] = [
      CurrentPerfOnlyUpdate(BOT_1_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_4_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_1_PERF_BULLET),
      CurrentPerfOnlyUpdate(BOT_1_PERF_BULLET),
    ]
    leaderboard_rows = generator.create_ranked_rows(updates)
    expected_leaderboard_rows = [
      LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3000, True),
      LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3000, True),
      LeaderboardRow(BOT_1_PERF_BULLET, 1, 0, 0, 1, 3000, True),
      LeaderboardRow(BOT_4_PERF_BULLET, 4, 0, 0, 4, 2800, True),
    ]
    self.assertListEqual(leaderboard_rows, expected_leaderboard_rows)


class TestLeaderboardGenerator(unittest.TestCase):
  """Tests for LeaderboardGenerator."""

  def test_create_all_leaderboards(self) -> None:
    file_system = InMemoryFileSystem()
    bullet_leaderboard = [BOT_1_ROW_BULLET.to_psv(), BOT_2_ROW_BULLET.to_psv()]
    file_system.save_file_lines(generator.get_psv_file_name(PerfType.BULLET), bullet_leaderboard)
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots("\n".join([remove_whitespace(BOT_1_CURRENT_JSON), remove_whitespace(BOT_2_CURRENT_JSON)]))
    date_provider = FakeDateProvider()
    date_provider.set_current_date("2025-04-01")
    leaderboard_generator = LeaderboardGenerator(file_system, lichess_client, date_provider)
    leaderboard_generator.generate_leaderboard_data()
    saved_leaderboard = file_system.load_file_lines(generator.get_psv_file_name(PerfType.BULLET))
    expected_leaderboard = [
      "Bot-2|||3000|0|0|1000|2022-04-01|2025-04-01|False|False|1|1|100|1|3000|False",
      "Bot-1|flair|_earth|2950|42|-50|1100|2024-04-01|2025-04-01|True|False|2|-1|-50|1|3000|False",
    ]
    self.assertEqual(saved_leaderboard, expected_leaderboard)
