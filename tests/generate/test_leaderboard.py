"""Tests for leaderboard.py."""

import unittest

from src.generate.leaderboard import LeaderboardPerf, LeaderboardRow
from src.generate.online_bot_user import OnlineBotUser, Perf, PerfType


TEST_BULLET_PERF = Perf(PerfType.BULLET, 100, 1450, False)
TEST_ONLINE_BOT_USER = OnlineBotUser("Bot1", [TEST_BULLET_PERF])

TOP_BOT = LeaderboardPerf("Top Bot", 1800, 400, "2021-04-01", "2025-10-12")
FIRST_MIDDLE_BOT = LeaderboardPerf("First Middle Bot", 1500, 100, "2022-04-01", "2025-10-12")
SECOND_MIDDLE_BOT = LeaderboardPerf("Second Middle Bot", 1500, 200, "2023-04-01", "2025-10-12")
BOTTOM_BOT = LeaderboardPerf("Bottom Bot", 1200, 300, "2025-04-01", "2025-10-12")


class TestLeaderboard(unittest.TestCase):
  def test_create_perfs_grouped_by_perf_type_with_three_perfs_creates_correct_leaderboard_perfs(self) -> None:
    leaderboard_perf = LeaderboardPerf.from_online_bot_user(TEST_ONLINE_BOT_USER, TEST_BULLET_PERF)
    self.assertEqual(leaderboard_perf, LeaderboardPerf("Bot1", 1450, 100, "TODO", "TODO"))

  def test_leaderboard_row_from_psv(self) -> None:
    leaderboard_row = LeaderboardRow.from_psv("Bot1|1500|100|2024-04-01|2025-04-01|4|1|50|3|1600")
    expected_perf = LeaderboardPerf("Bot1", 1500, 100, "2024-04-01", "2025-04-01")
    expected_leaderboard_row = LeaderboardRow(expected_perf, 4, 1, 50, 3, 1600)
    self.assertEqual(leaderboard_row, expected_leaderboard_row)

  def test_create_leaderboard_rows_with_one_perf_creates_correct_row(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([TOP_BOT])
    self.assertEqual(len(leaderboard_rows), 1)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))

  def test_create_leaderboard_rows_with_three_perfs_has_correct_ranking(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([FIRST_MIDDLE_BOT, BOTTOM_BOT, TOP_BOT])
    self.assertEqual(len(leaderboard_rows), 3)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(FIRST_MIDDLE_BOT, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[2], LeaderboardRow(BOTTOM_BOT, 3, 0, 0, 3, 1200))

  def test_create_leaderboard_rows_with_tied_ratings_has_correct_rankings(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([SECOND_MIDDLE_BOT, BOTTOM_BOT, TOP_BOT, FIRST_MIDDLE_BOT])
    self.assertEqual(len(leaderboard_rows), 4)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(FIRST_MIDDLE_BOT, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[2], LeaderboardRow(SECOND_MIDDLE_BOT, 2, 0, 0, 2, 1500))
    self.assertEqual(leaderboard_rows[3], LeaderboardRow(BOTTOM_BOT, 4, 0, 0, 4, 1200))

  def test_create_leaderboard_rows_with_three_way_tie_has_correct_rankings(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([BOTTOM_BOT, TOP_BOT, TOP_BOT, TOP_BOT])
    self.assertEqual(len(leaderboard_rows), 4)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[1], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))
    self.assertEqual(leaderboard_rows[3], LeaderboardRow(BOTTOM_BOT, 4, 0, 0, 4, 1200))
