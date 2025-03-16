"""Tests for leaderboard.py."""

import unittest

from src.generate.leaderboard_data import (
  CurrentPerfOnlyUpdate,
  FullUpdate,
  LeaderboardPerf,
  LeaderboardRow,
  LeaderboardUpdate,
  PreviousRowOnlyUpdate,
)
from src.generate.lichess_bot_user import BotUser, Perf, PerfType


def create_perf(username: str, rating: int, games: int, created_date: str) -> LeaderboardPerf:
  """Create a perf with several default values set."""
  return LeaderboardPerf(username, "", "", rating, 0, 0, games, created_date, "2025-04-01", False, False)


BOT_1_LICHESS_PERF = Perf(PerfType.BULLET, 100, 1450, 0, 0, False)
BOT_1_BOT_USER = BotUser("Bot1", "", "", "2024-01-01", False, False, [BOT_1_LICHESS_PERF])

BOT_2_PERF = create_perf("Bot-2", 1800, 400, "2021-04-01")
BOT_2_ROW = LeaderboardRow(BOT_2_PERF, 1, 0, 0, 1, 1800, False, True)


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPeft."""

  def test_from_bot_user(self) -> None:
    leaderboard_perf = LeaderboardPerf.from_bot_user(BOT_1_BOT_USER, BOT_1_LICHESS_PERF, "2025-04-01")
    self.assertEqual(leaderboard_perf, create_perf("Bot1", 1450, 100, "2024-01-01"))


class TestLeaderboardRow(unittest.TestCase):
  """Tests for LeaderboardRow."""

  def test_from_json(self) -> None:
    leaderboard_row = LeaderboardRow.from_json(
      """
      {
        "perf": {
          "username": "Bot1",
          "flair": "flair",
          "flag": "flag",
          "rating": 1500,
          "rd": 12,
          "prog": 34,
          "games": 100,
          "created_date": "2024-04-01",
          "last_seen_date": "2025-04-01"
        },
        "rank": 4,
        "rank_delta": 1,
        "rating_delta": 50,
        "peak_rank": 3,
        "peak_rating": 1600,
        "is_online": true
      }
      """
    )
    expected_perf = LeaderboardPerf("Bot1", "flair", "flag", 1500, 12, 34, 100, "2024-04-01", "2025-04-01", False, False)
    expected_leaderboard_row = LeaderboardRow(expected_perf, 4, 1, 50, 3, 1600, False, True)
    self.assertEqual(leaderboard_row, expected_leaderboard_row)

  def test_to_json_round_trip(self) -> None:
    perf = LeaderboardPerf("Bot1", "flair", "EU", 1500, 12, 34, 100, "2024-04-01", "2025-04-01", True, True)
    leaderboard_row = LeaderboardRow(perf, 4, 1, 50, 3, 1600, True, False)
    self.assertEqual(LeaderboardRow.from_json(leaderboard_row.to_json()), leaderboard_row)


class TestLeaderboardUpdate(unittest.TestCase):
  """Tests for LeaderboardUpdate and subclasses."""

  def test_from_previous_row_and_current_perf(self) -> None:
    self.assertIsInstance(LeaderboardUpdate.create_update(BOT_2_ROW, BOT_2_PERF), FullUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(BOT_2_ROW, None), PreviousRowOnlyUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(None, BOT_2_PERF), CurrentPerfOnlyUpdate)
    self.assertRaises(ValueError, lambda: LeaderboardUpdate.create_update(None, None))

  def test_row_only_update(self) -> None:
    previous_perf = create_perf("Bot 1", 1500, 100, "2024-01-01")
    previous_row = LeaderboardRow(previous_perf, 5, 0, 0, 3, 1500, True, True)
    update = PreviousRowOnlyUpdate(previous_row)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_perf, 2, 3, 0, 2, 1500, False, False))

  def test_perf_only_update(self) -> None:
    previous_perf = create_perf("Bot 1", 1500, 100, "2024-01-01")
    update = CurrentPerfOnlyUpdate(previous_perf)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_perf, 2, 0, 0, 2, 1500, True, True))

  def test_full_update(self) -> None:
    previous_perf = create_perf("Bot 1", 1500, 100, "2024-01-01")
    previous_row = LeaderboardRow(previous_perf, 5, 0, 0, 3, 1500, True, True)
    current_perf = create_perf("Bot 1", 1600, 120, "2024-01-01")
    update = FullUpdate(previous_row, current_perf)
    self.assertEqual(update.get_rating(), 1600)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(1), LeaderboardRow(current_perf, 1, 4, 100, 1, 1600, False, True))
