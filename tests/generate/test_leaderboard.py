"""Tests for leaderboard.py."""

import unittest

from src.generate.leaderboard import LeaderboardBotInfo, LeaderboardRow
from src.generate.online_bot_user import OnlineBotUser, Perf, PerfType


TEST_OBU_1 = OnlineBotUser(
  "Bot1",
  [Perf(PerfType.BULLET, 100, 1450, False), Perf(PerfType.BLITZ, 200, 1500, False), Perf(PerfType.RAPID, 300, 1550, False)],
)

TOP_BOT = LeaderboardBotInfo("Top Bot", 1800, 400, "2021-04-01", "2025-10-12")
FIRST_MIDDLE_BOT = LeaderboardBotInfo("First Middle Bot", 1500, 100, "2022-04-01", "2025-10-12")
SECOND_MIDDLE_BOT = LeaderboardBotInfo("Second Middle Bot", 1500, 200, "2023-04-01", "2025-10-12")
BOTTOM_BOT = LeaderboardBotInfo("Bottom Bot", 1200, 300, "2025-04-01", "2025-10-12")


class TestLeaderboard(unittest.TestCase):
  def test_create_bot_info_dict_with_three_perfs_creates_correct_dict(self) -> None:
    bot_info_dict = LeaderboardBotInfo.create_bot_info_dict(TEST_OBU_1)
    self.assertEqual(len(bot_info_dict), 3)
    self.assertEqual(bot_info_dict[PerfType.BULLET], LeaderboardBotInfo("Bot1", 1450, 100, "TODO", "TODO"))
    self.assertEqual(bot_info_dict[PerfType.BLITZ], LeaderboardBotInfo("Bot1", 1500, 200, "TODO", "TODO"))
    self.assertEqual(bot_info_dict[PerfType.RAPID], LeaderboardBotInfo("Bot1", 1550, 300, "TODO", "TODO"))

  def test_create_leaderboard_rows_with_one_bot_info_creates_correct_row(self) -> None:
    leaderboard_rows = LeaderboardRow.create_leaderboard_rows([TOP_BOT])
    self.assertEqual(len(leaderboard_rows), 1)
    self.assertEqual(leaderboard_rows[0], LeaderboardRow(TOP_BOT, 1, 0, 0, 1, 1800))

  def test_create_leaderboard_rows_with_three_bot_infos_has_correct_ranking(self) -> None:
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
