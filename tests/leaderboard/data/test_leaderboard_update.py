"""Tests for leaderboard_update.py."""

import unittest

from src.leaderboard.data.leaderboard_data import LeaderboardPerf, LeaderboardRow
from src.leaderboard.data.leaderboard_update import CurrentPerfOnlyUpdate, FullUpdate, LeaderboardUpdate, PreviousRowOnlyUpdate


def create_perf(username: str, rating: int, games: int, created_date: str) -> LeaderboardPerf:
  """Create a perf with several default values set."""
  return LeaderboardPerf(username, "", "", rating, 0, 0, games, created_date, "2025-04-01", False, False)


BOT_2_PERF = create_perf("Bot-2", 1800, 400, "2021-04-01")
BOT_2_ROW = LeaderboardRow(BOT_2_PERF, 1, 0, 0, 1, 1800, False, True)


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
