"""Tests for leaderboard_update.py."""

import unittest

from src.leaderboard.data.leaderboard_row import BotPerf, LeaderboardPerf, LeaderboardRow, RankInfo
from src.leaderboard.data.leaderboard_update import (
  CurrentBotPerfOnlyUpdate,
  FullUpdate,
  LeaderboardUpdate,
  PreviousRowOnlyUpdate,
)


def create_bot_perf(name: str, rating: int, games: int) -> BotPerf:
  """Create a BotPerf with several default values set."""
  return BotPerf(name, LeaderboardPerf(rating, 0, 0, games, False))


class TestLeaderboardUpdate(unittest.TestCase):
  """Tests for LeaderboardUpdate and subclasses."""

  def test_check_is_eligible(self) -> None:
    self.assertTrue(LeaderboardUpdate.check_is_eligible(False))
    self.assertFalse(LeaderboardUpdate.check_is_eligible(True))

  def test_from_previous_row_and_current_bot_perf(self) -> None:
    bot_perf = create_bot_perf("Bot 1", 1800, 400)
    bot_row = LeaderboardRow("Bot 1", bot_perf.perf, RankInfo(1, 0, 0, 0, 1, 1800))
    self.assertIsInstance(LeaderboardUpdate.create_update(bot_row, bot_perf), FullUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(bot_row, None), PreviousRowOnlyUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(None, bot_perf), CurrentBotPerfOnlyUpdate)
    self.assertRaises(ValueError, lambda: LeaderboardUpdate.create_update(None, None))

  def test_row_only_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100)
    previous_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(5, -1, -10, 4, 3, 1500))
    update = PreviousRowOnlyUpdate(previous_row)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertTrue(update.is_eligible())
    expected_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(2, 3, 0, 0, 2, 1500))
    self.assertEqual(update.to_leaderboard_row(2), expected_row)

  def test_bot_perf_only_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100)
    update = CurrentBotPerfOnlyUpdate(previous_bot_perf)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertTrue(update.is_eligible())
    expected_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(2, 0, 0, 0, 2, 1500))
    self.assertEqual(update.to_leaderboard_row(2), expected_row)

  def test_full_update(self) -> None:
    previous_bot_perf = create_bot_perf("Bot 1", 1500, 100)
    previous_row = LeaderboardRow("Bot 1", previous_bot_perf.perf, RankInfo(5, 0, 0, 0, 3, 1500))
    current_bot_perf = create_bot_perf("Bot 1", 1600, 120)
    update = FullUpdate(previous_row, current_bot_perf)
    self.assertEqual(update.get_rating(), 1600)
    self.assertEqual(update.get_name(), "Bot 1")
    self.assertTrue(update.is_eligible())
    expected_row = LeaderboardRow("Bot 1", current_bot_perf.perf, RankInfo(1, 4, 100, 20, 1, 1600))
    self.assertEqual(update.to_leaderboard_row(1), expected_row)
