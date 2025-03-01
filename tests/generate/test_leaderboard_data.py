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


TEST_BULLET_LICHESS_PERF = Perf(PerfType.BULLET, 100, 1450, False)
TEST_BOT_USER = BotUser("Bot1", [TEST_BULLET_LICHESS_PERF])

TOP_BOT_PERF = LeaderboardPerf("Top Bot", 1800, 400, "2021-04-01", "2025-10-12")
FIRST_MIDDLE_BOT_PERF = LeaderboardPerf("First Middle Bot", 1500, 100, "2022-04-01", "2025-10-12")
SECOND_MIDDLE_BOT_PERF = LeaderboardPerf("Second Middle Bot", 1500, 200, "2023-04-01", "2025-10-12")
BOTTOM_BOT_PERF = LeaderboardPerf("Bottom Bot", 1200, 300, "2025-04-01", "2025-10-12")


TOP_BOT_ROW = LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1500)


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPeft."""

  def test_from_bot_user(self) -> None:
    leaderboard_perf = LeaderboardPerf.from_bot_user(TEST_BOT_USER, TEST_BULLET_LICHESS_PERF)
    self.assertEqual(leaderboard_perf, LeaderboardPerf("Bot1", 1450, 100, "TODO", "TODO"))


class TestLeaderboardRow(unittest.TestCase):
  """Tests for LeaderboardRow."""

  def test_from_psv(self) -> None:
    leaderboard_row = LeaderboardRow.from_psv("Bot1|1500|100|2024-04-01|2025-04-01|4|1|50|3|1600")
    expected_perf = LeaderboardPerf("Bot1", 1500, 100, "2024-04-01", "2025-04-01")
    expected_leaderboard_row = LeaderboardRow(expected_perf, 4, 1, 50, 3, 1600)
    self.assertEqual(leaderboard_row, expected_leaderboard_row)

  def test_to_psv(self) -> None:
    perf = LeaderboardPerf("Bot1", 1500, 100, "2024-04-01", "2025-04-01")
    leaderboard_row = LeaderboardRow(perf, 4, 1, 50, 3, 1600)
    expected_psv = "Bot1|1500|100|2024-04-01|2025-04-01|4|1|50|3|1600"
    self.assertEqual(leaderboard_row.to_psv(), expected_psv)

  def test_create_leaderboard_rows_with_one_perf(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([TOP_BOT_PERF])
    self.assertEqual(len(leaderboard_rows), 1)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))

  def test_create_leaderboard_rows_with_three_perfs(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([FIRST_MIDDLE_BOT_PERF, BOTTOM_BOT_PERF, TOP_BOT_PERF])
    self.assertEqual(len(leaderboard_rows), 3)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(FIRST_MIDDLE_BOT_PERF, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[2], LeaderboardRow(BOTTOM_BOT_PERF, 3, 0, 0, 3, 1200))

  def test_create_leaderboard_rows_with_tied_ratings(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows(
      [SECOND_MIDDLE_BOT_PERF, BOTTOM_BOT_PERF, TOP_BOT_PERF, FIRST_MIDDLE_BOT_PERF]
    )
    self.assertEqual(len(leaderboard_rows), 4)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(FIRST_MIDDLE_BOT_PERF, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[2], LeaderboardRow(SECOND_MIDDLE_BOT_PERF, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[3], LeaderboardRow(BOTTOM_BOT_PERF, 4, 0, 0, 4, 1200))

  def test_create_leaderboard_rows_with_three_way_tie(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([BOTTOM_BOT_PERF, TOP_BOT_PERF, TOP_BOT_PERF, TOP_BOT_PERF])
    self.assertEqual(len(leaderboard_rows), 4)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(TOP_BOT_PERF, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[3], LeaderboardRow(BOTTOM_BOT_PERF, 4, 0, 0, 4, 1200))


class TestLeaderboardUpdate(unittest.TestCase):
  """Tests for LeaderboardUpdate and subclasses."""

  def test_from_previous_row_and_current_perf(self) -> None:
    self.assertIsInstance(LeaderboardUpdate.create_update(TOP_BOT_ROW, TOP_BOT_PERF), FullUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(TOP_BOT_ROW, None), PreviousRowOnlyUpdate)
    self.assertIsInstance(LeaderboardUpdate.create_update(None, TOP_BOT_PERF), CurrentPerfOnlyUpdate)
    self.assertRaises(ValueError, lambda: LeaderboardUpdate.create_update(None, None))

  def test_row_only_update(self) -> None:
    previous_perf = LeaderboardPerf("Bot 1", 1500, 100, "2024-01-01", "2025-01-01")
    previous_row = LeaderboardRow(previous_perf, 5, 0, 0, 3, 1500)
    update = PreviousRowOnlyUpdate(previous_row)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_perf, 2, 3, 0, 2, 1500))

  def test_perf_only_update(self) -> None:
    previous_perf = LeaderboardPerf("Bot 1", 1500, 100, "2024-01-01", "2025-01-01")
    update = CurrentPerfOnlyUpdate(previous_perf)
    self.assertEqual(update.get_rating(), 1500)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(2), LeaderboardRow(previous_perf, 2, 0, 0, 2, 1500))

  def test_full_update(self) -> None:
    previous_perf = LeaderboardPerf("Bot 1", 1500, 100, "2024-01-01", "2025-01-01")
    previous_row = LeaderboardRow(previous_perf, 5, 0, 0, 3, 1500)
    current_perf = LeaderboardPerf("Bot 1", 1600, 120, "2024-01-01", "2024-01-02")
    update = FullUpdate(previous_row, current_perf)
    self.assertEqual(update.get_rating(), 1600)
    self.assertEqual(update.get_created_date(), "2024-01-01")
    self.assertEqual(update.to_leaderboard_row(1), LeaderboardRow(current_perf, 1, 4, 100, 1, 1600))
