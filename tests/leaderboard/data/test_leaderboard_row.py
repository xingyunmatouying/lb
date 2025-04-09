"""Tests for leaderboard_row.py."""

import unittest

from src.leaderboard.data.leaderboard_row import BotInfo, BotProfile, LeaderboardPerf, LeaderboardRowLite, RankInfo
from src.leaderboard.li.bot_user import BotUser, Perf
from src.leaderboard.li.pert_type import PerfType
from tests.leaderboard.chrono.epoch_seconds import DATE_2024_01_01, DATE_2025_04_01


EMPTY_BOT_PROFILE = BotProfile("", "", "", 0, 0, False, False)
EMPTY_LEADERBOARD_PERF = LeaderboardPerf(0, 0, 0, 0)


class TestBotProfile(unittest.TestCase):
  """Tests for BotProfile."""

  def test_from_perf(self) -> None:
    bot_user = BotUser("Bot1", "flair", "flag", DATE_2024_01_01, True, True, [])
    self.assertEqual(
      BotProfile.from_bot_user(bot_user, DATE_2025_04_01),
      BotProfile("Bot1", "flair", "flag", DATE_2024_01_01, DATE_2025_04_01, True, True),
    )

  def test_from_json_dict(self) -> None:
    json_dict = {
      "username": "Bot1",
      "flair": "flair",
      "flag": "FR",
      "created_time": DATE_2024_01_01,
      "last_seen_time": DATE_2025_04_01,
      "patron": True,
      "tos_violation": True,
    }
    self.assertEqual(
      BotProfile.from_json_dict(json_dict), BotProfile("Bot1", "flair", "FR", DATE_2024_01_01, DATE_2025_04_01, True, True)
    )

  def test_from_json_dict_default(self) -> None:
    self.assertEqual(BotProfile.from_json_dict({}), EMPTY_BOT_PROFILE)


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPerf."""

  def test_from_perf(self) -> None:
    perf = Perf(PerfType.BULLET, 100, 1450, 25, -10, False)
    self.assertEqual(LeaderboardPerf.from_perf(perf), LeaderboardPerf(1450, 25, -10, 100))

  def test_from_json_dict(self) -> None:
    json_dict = {"rating": 1450, "rd": 25, "prog": -10, "games": 100}
    self.assertEqual(LeaderboardPerf.from_json_dict(json_dict), LeaderboardPerf(1450, 25, -10, 100))

  def test_from_json_dict_default(self) -> None:
    self.assertEqual(LeaderboardPerf.from_json_dict({}), EMPTY_LEADERBOARD_PERF)


class TestBotInfo(unittest.TestCase):
  """Tests for BotInfo."""

  def test_create_bot_info(self) -> None:
    perf = Perf(PerfType.BULLET, 0, 1500, 0, 0, False)
    bot_user = BotUser("Bot1", "", "", 0, False, False, [])
    bot_info = BotInfo.create_bot_info(bot_user, perf, DATE_2025_04_01)
    self.assertEqual(
      bot_info, BotInfo(BotProfile("Bot1", "", "", 0, DATE_2025_04_01, False, False), LeaderboardPerf(1500, 0, 0, 0))
    )

  def test_from_json_dict(self) -> None:
    json_dict = {"profile": {"username": "Bot1", "last_seen_time": DATE_2025_04_01}, "perf": {"rating": 1500}}
    self.assertEqual(
      BotInfo.from_json_dict(json_dict),
      BotInfo(BotProfile("Bot1", "", "", 0, DATE_2025_04_01, False, False), LeaderboardPerf(1500, 0, 0, 0)),
    )

  def test_from_json_dict_default(self) -> None:
    self.assertEqual(BotInfo.from_json_dict({}), BotInfo(EMPTY_BOT_PROFILE, EMPTY_LEADERBOARD_PERF))


class TestLeaderboardRowLite(unittest.TestCase):
  """Tests for LeaderboardRowLite."""

  def test_from_json(self) -> None:
    leaderboard_row_json = """
      {
        "username": "Bot1",
        "perf": {
          "rating": 1500
        },
        "rank_info": {
          "rank": 4,
          "delta_rank": 1,
          "delta_rating": 50,
          "peak_rank": 3,
          "peak_rating": 1600,
          "is_online": true
        }
      }
      """
    expected_perf = LeaderboardPerf(1500, 0, 0, 0)
    expected_leaderboard_row = LeaderboardRowLite("Bot1", expected_perf, RankInfo(4, 1, 50, 3, 1600, False, True))
    self.assertEqual(LeaderboardRowLite.from_json(leaderboard_row_json), expected_leaderboard_row)

  def test_to_json_round_trip(self) -> None:
    leaderboard_row = LeaderboardRowLite("Bot1", LeaderboardPerf(1500, 12, 34, 100), RankInfo(4, 1, 50, 3, 1600, True, False))
    self.assertEqual(LeaderboardRowLite.from_json(leaderboard_row.to_json()), leaderboard_row)
