"""Tests for leaderboard_row.py."""

import unittest

from src.leaderboard.data.leaderboard_row import BotInfo, BotProfile, LeaderboardPerf, LeaderboardRow
from src.leaderboard.li.bot_user import BotUser, Perf, PerfType


EMPTY_BOT_PROFILE = BotProfile("", "", "", "", False, False)
EMPTY_LEADERBOARD_PERF = LeaderboardPerf(0, 0, 0, 0)


class TestBotProfile(unittest.TestCase):
  """Tests for BotProfile."""

  def test_from_perf(self) -> None:
    bot_user = BotUser("Bot1", "flair", "flag", "2024-01-01", True, True, [])
    self.assertEqual(BotProfile.from_bot_user(bot_user), BotProfile("Bot1", "flair", "flag", "2024-01-01", True, True))

  def test_from_json(self) -> None:
    json_dict = {
      "username": "Bot1",
      "flair": "flair",
      "flag": "FR",
      "created_date": "2024-01-01",
      "patron": True,
      "tos_violation": True,
    }
    self.assertEqual(BotProfile.from_json(json_dict), BotProfile("Bot1", "flair", "FR", "2024-01-01", True, True))

  def test_from_json_default(self) -> None:
    self.assertEqual(BotProfile.from_json({}), EMPTY_BOT_PROFILE)


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPerf."""

  def test_from_perf(self) -> None:
    perf = Perf(PerfType.BULLET, 100, 1450, 25, -10, False)
    self.assertEqual(LeaderboardPerf.from_perf(perf), LeaderboardPerf(1450, 25, -10, 100))

  def test_from_json(self) -> None:
    json_dict = {"rating": 1450, "rd": 25, "prog": -10, "games": 100}
    self.assertEqual(LeaderboardPerf.from_json(json_dict), LeaderboardPerf(1450, 25, -10, 100))

  def test_from_json_default(self) -> None:
    self.assertEqual(LeaderboardPerf.from_json({}), EMPTY_LEADERBOARD_PERF)


class TestBotInfo(unittest.TestCase):
  """Tests for BotInfo."""

  def test_create_bot_info(self) -> None:
    perf = Perf(PerfType.BULLET, 0, 1500, 0, 0, False)
    bot_user = BotUser("Bot1", "", "", "", False, False, [])
    bot_info = BotInfo.create_bot_info(bot_user, perf, "2025-04-01")
    self.assertEqual(
      bot_info, BotInfo(BotProfile("Bot1", "", "", "", False, False), LeaderboardPerf(1500, 0, 0, 0), "2025-04-01")
    )

  def test_from_json(self) -> None:
    json_dict = {"profile": {"username": "Bot1"}, "perf": {"rating": 1500}, "last_seen_date": "2025-04-01"}
    self.assertEqual(
      BotInfo.from_json(json_dict),
      BotInfo(BotProfile("Bot1", "", "", "", False, False), LeaderboardPerf(1500, 0, 0, 0), "2025-04-01"),
    )

  def test_from_json_default(self) -> None:
    self.assertEqual(BotInfo.from_json({}), BotInfo(EMPTY_BOT_PROFILE, EMPTY_LEADERBOARD_PERF, ""))


class TestLeaderboardRow(unittest.TestCase):
  """Tests for LeaderboardRow."""

  def test_from_json(self) -> None:
    leaderboard_row_json = """
      {
        "bot_info": {
          "profile": {
            "username": "Bot1"
          },
          "perf": {
            "rating": 1500
          },
          "last_seen_date": "2025-04-01"
        },
        "rank": 4,
        "delta_rank": 1,
        "delta_rating": 50,
        "peak_rank": 3,
        "peak_rating": 1600,
        "is_online": true
      }
      """
    expected_bot_info = BotInfo(BotProfile("Bot1", "", "", "", False, False), LeaderboardPerf(1500, 0, 0, 0), "2025-04-01")
    expected_leaderboard_row = LeaderboardRow(expected_bot_info, 4, 1, 50, 3, 1600, False, True)
    self.assertEqual(LeaderboardRow.from_json(leaderboard_row_json), expected_leaderboard_row)

  def test_to_json_round_trip(self) -> None:
    bot_info = BotInfo(
      BotProfile("Bot1", "flair", "EU", "2024-04-01", False, False), LeaderboardPerf(1500, 12, 34, 100), "2025-04-01"
    )
    leaderboard_row = LeaderboardRow(bot_info, 4, 1, 50, 3, 1600, True, False)
    self.assertEqual(LeaderboardRow.from_json(leaderboard_row.to_json()), leaderboard_row)
