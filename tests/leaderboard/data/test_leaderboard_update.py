"""Tests for leaderboard_update.py."""

import unittest

from src.leaderboard.data.leaderboard_row import BotInfo, BotProfile, LeaderboardPerf, LeaderboardRow
from src.leaderboard.data.leaderboard_update import (
  CurrentBotInfoOnlyUpdate,
  FullUpdate,
  LeaderboardUpdate,
  PreviousRowOnlyUpdate,
)


def create_bot_info(username: str, rating: int, games: int, created_date: str) -> BotInfo:
  """Create a BotInfo with several default values set."""
  return BotInfo(BotProfile(username, "", "", created_date, False, False), LeaderboardPerf(rating, 0, 0, games), "2025-04-01")


BOT_2_INFO = create_bot_info("Bot-2", 1800, 400, "2021-04-01")
BOT_2_ROW = LeaderboardRow(BOT_2_INFO, 1, 0, 0, 1, 1800, False, True)


class TestLeaderboardUpdate(unittest.TestCase):
  """Tests for LeaderboardUpdate and subclasses."""

  def test_from_previous_row_and_current_bot_info(self) -> None:
    self.assertIsInstance(LeaderboardUpdate.create_update(BOT_2_ROW, BOT_2_INFO), FullUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(BOT_2_ROW, None), PreviousRowOnlyUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(None, BOT_2_INFO), CurrentBotInfoOnlyUpdate)
    self.assertRaises(ValueError, lambda: LeaderboardUpdate.create_update(None, None))

  def test_row_only_update(self) -> None:
    previous_bot_info = create_bot_info("Bot 1", 1500, 100, "2024-01-01")
    previous_row = LeaderboardRow(previous_bot_info, 5, 0, 0, 3, 1500, True, True)
    update = PreviousRowOnlyUpdate(previous_row)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_bot_info, 2, 3, 0, 2, 1500, False, False))

  def test_bot_info_only_update(self) -> None:
    previous_bot_info = create_bot_info("Bot 1", 1500, 100, "2024-01-01")
    update = CurrentBotInfoOnlyUpdate(previous_bot_info)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_bot_info, 2, 0, 0, 2, 1500, True, True))

  def test_full_update(self) -> None:
    previous_bot_info = create_bot_info("Bot 1", 1500, 100, "2024-01-01")
    previous_row = LeaderboardRow(previous_bot_info, 5, 0, 0, 3, 1500, True, True)
    current_bot_info = create_bot_info("Bot 1", 1600, 120, "2024-01-01")
    update = FullUpdate(previous_row, current_bot_info)
    self.assertEqual(update.get_rating(), 1600)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(1), LeaderboardRow(current_bot_info, 1, 4, 100, 1, 1600, False, True))
