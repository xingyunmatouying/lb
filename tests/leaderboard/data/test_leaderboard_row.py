"""Tests for leaderboard_row.py."""

import unittest

from src.leaderboard.data.leaderboard_row import LeaderboardPerf, LeaderboardRow
from src.leaderboard.li.bot_user import BotUser, Perf, PerfType


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPeft."""

  def test_from_bot_user(self) -> None:
    perf = Perf(PerfType.BULLET, 100, 1450, 0, 0, False)
    bot_user = BotUser("Bot1", "", "", "2024-01-01", False, False, [perf])
    leaderboard_perf = LeaderboardPerf.from_bot_user(bot_user, perf, "2025-04-01")
    self.assertEqual(
      leaderboard_perf, LeaderboardPerf("Bot1", "", "", 1450, 0, 0, 100, "2024-01-01", "2025-04-01", False, False)
    )


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
