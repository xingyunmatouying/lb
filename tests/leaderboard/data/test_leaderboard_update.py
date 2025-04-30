"""Tests for leaderboard_update.py."""

import unittest

from src.leaderboard.data.leaderboard_row import BotPerf, LeaderboardPerf, LeaderboardRow, RankInfo
from src.leaderboard.data.leaderboard_update import (
  CurrentBotPerfOnlyUpdate,
  FullUpdate,
  LeaderboardUpdate,
  PreviousRowOnlyUpdate,
)
from tests.leaderboard.chrono.epoch_seconds import DATE_2024_04_01, DATE_2025_04_01


def create_bot_perf(name: str, rating: int, games: int, rd: int) -> BotPerf:
  """Create a BotPerf with several default values set."""
  return BotPerf(name, LeaderboardPerf(rating, rd, 0, games, False))


class TestLeaderboardUpdate(unittest.TestCase):
  """Tests for LeaderboardUpdate and subclasses."""

  def test_check_is_eligible(self) -> None:
    self.assertTrue(LeaderboardUpdate.check_is_eligible(False, DATE_2025_04_01, DATE_2025_04_01))
    self.assertFalse(LeaderboardUpdate.check_is_eligible(True, DATE_2025_04_01, DATE_2025_04_01))
    self.assertFalse(LeaderboardUpdate.check_is_eligible(False, DATE_2024_04_01, DATE_2025_04_01))
    self.assertFalse(LeaderboardUpdate.check_is_eligible(True, DATE_2024_04_01, DATE_2025_04_01))

  def test_from_previous_row_and_current_bot_perf(self) -> None:
    bot_perf = create_bot_perf("Bot 1", 1800, 400, 45)
    bot_row = LeaderboardRow("Bot 1", bot_perf.perf, RankInfo(1, 0, 0, 0, 1, 1800, DATE_2025_04_01))
    self.assertIsInstance(LeaderboardUpdate.create_update(bot_row, bot_perf), FullUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(bot_row, None), PreviousRowOnlyUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(None, bot_perf), CurrentBotPerfOnlyUpdate)
    self.assertRaises(ValueError, lambda: LeaderboardUpdate.create_update(None, None))

  def test_row_only_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100, 45)
    previous_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(5, -1, -10, 4, 3, 1500, DATE_2025_04_01))
    update = PreviousRowOnlyUpdate(previous_row)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_rd(), 45)
    self.assertTrue(update.is_eligible(DATE_2025_04_01))
    expected_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(2, 3, 0, 0, 2, 1500, DATE_2025_04_01))
    self.assertEqual(update.to_leaderboard_row(2, DATE_2025_04_01), expected_row)

  def test_bot_perf_only_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100, 45)
    update = CurrentBotPerfOnlyUpdate(previous_bot_perf)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_rd(), 45)
    self.assertTrue(update.is_eligible(DATE_2025_04_01))
    expected_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(2, 0, 0, 0, 2, 1500, DATE_2025_04_01))
    self.assertEqual(update.to_leaderboard_row(2, DATE_2025_04_01), expected_row)

  def test_full_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100, 45)
    previous_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(5, 0, 0, 0, 3, 1500, DATE_2024_04_01))
    current_bot_perf = create_bot_perf("Bot 1", 1600, 120, 60)
    update = FullUpdate(previous_row, current_bot_perf)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertEqual(update.get_rating(), 1600)
    self.assertEqual(update.get_rd(), 60)
    self.assertTrue(update.is_eligible(DATE_2025_04_01))
    expected_row = LeaderboardRow("Bot 1", current_bot_perf.perf, RankInfo(1, 4, 100, 20, 1, 1600, DATE_2025_04_01))
    self.assertEqual(update.to_leaderboard_row(1, DATE_2025_04_01), expected_row)

  def test_full_update_no_games_played(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100, 45)
    previous_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(5, 0, 0, 0, 3, 1500, DATE_2024_04_01))
    # Reuse the same perf as it has not changed (most crucially, delta games is zero)
    update = FullUpdate(previous_row, previous_bot_perf)
    expected_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(6, -1, 0, 0, 5, 1500, DATE_2024_04_01))
    self.assertEqual(update.to_leaderboard_row(6, DATE_2025_04_01), expected_row)
