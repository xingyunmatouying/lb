"""Tests for leaderboard_objects.py."""

import unittest

from src.leaderboard.data.leaderboard_objects import BotProfile, LeaderboardPerf, LeaderboardRow, RankInfo
from src.leaderboard.li.bot_user import BotUser, Perf
from src.leaderboard.li.pert_type import PerfType
from tests.leaderboard.chrono import epoch_seconds
from tests.leaderboard.chrono.epoch_seconds import DATE_2024_01_01, DATE_2025_04_01


class TestBotProfile(unittest.TestCase):
  """Tests for BotProfile."""

  def test_from_perf(self) -> None:
    bot_user = BotUser("Bot1", "flair", "flag", DATE_2024_01_01, DATE_2025_04_01, True, True, [])
    self.assertEqual(
      BotProfile.from_bot_user(bot_user),
      BotProfile("Bot1", "flair", "flag", DATE_2024_01_01, DATE_2025_04_01, True, True, True, True),
    )

  def test_from_json_dict(self) -> None:
    json_dict = {
      "name": "Bot1",
      "flair": "flair",
      "flag": "FR",
      "created": DATE_2024_01_01,
      "last_seen": DATE_2025_04_01,
      "patron": True,
      "tos_violation": True,
      "new": True,
      "online": True,
    }
    expected_bot_profile = BotProfile("Bot1", "flair", "FR", DATE_2024_01_01, DATE_2025_04_01, True, True, False, False)
    self.assertEqual(BotProfile.from_json_dict(json_dict), expected_bot_profile)

  def test_create_updated_copy_for_for_merge(self) -> None:
    updated_copy = BotProfile("", "", "", 0, 0, False, False, True, True).create_updated_copy_for_for_merge()
    self.assertFalse(updated_copy.new)
    self.assertTrue(updated_copy.online)

  def test_is_eligible_last_seen(self) -> None:
    bot_profile = BotProfile("", "", "", 0, epoch_seconds.from_date(2025, 4, 1), False, False, True, True)
    self.assertTrue(bot_profile.is_eligible(epoch_seconds.from_date(2025, 4, 15)))
    self.assertFalse(bot_profile.is_eligible(epoch_seconds.from_date(2025, 4, 15) + 1))

  def test_is_eligible_tos_violation(self) -> None:
    bot_profile = BotProfile("", "", "", 0, DATE_2025_04_01, False, True, True, True)
    self.assertFalse(bot_profile.is_eligible(DATE_2025_04_01))

  def test_from_json_dict_default(self) -> None:
    self.assertEqual(BotProfile.from_json_dict({}), BotProfile("", "", "", 0, 0, False, False, False, False))


class TestLeaderboardPerf(unittest.TestCase):
  """Tests for LeaderboardPerf."""

  def test_from_perf(self) -> None:
    perf = Perf(PerfType.BULLET, 100, 1450, 25, -10, True)
    self.assertEqual(LeaderboardPerf.from_perf(perf), LeaderboardPerf(1450, 25, -10, 100, True))

  def test_from_json_dict(self) -> None:
    json_dict = {"rating": 1450, "rd": 25, "prog": -10, "games": 100, "prov": True}
    self.assertEqual(LeaderboardPerf.from_json_dict(json_dict), LeaderboardPerf(1450, 25, -10, 100, True))

  def test_from_json_dict_default(self) -> None:
    self.assertEqual(LeaderboardPerf.from_json_dict({}), LeaderboardPerf(0, 0, 0, 0, False))


class TestLeaderboardRow(unittest.TestCase):
  """Tests for LeaderboardRow."""

  def test_from_json(self) -> None:
    leaderboard_row_json = """
      {
        "name": "Bot1",
        "perf": {
          "rating": 1700,
          "rd": 115,
          "prog": 15,
          "games": 200,
          "prov": true
        },
        "rank_info": {
          "rank": 4,
          "delta_rank": 1,
          "delta_rating": 50,
          "delta_games": 10,
          "peak_rank": 3,
          "peak_rating": 1700,
          "last_played": 1743500000
        }
      }
      """
    expected_perf = LeaderboardPerf(1700, 115, 15, 200, True)
    expected_leaderboard_row = LeaderboardRow("Bot1", expected_perf, RankInfo(4, 1, 50, 10, 3, 1700, DATE_2025_04_01))
    self.assertEqual(LeaderboardRow.from_json(leaderboard_row_json), expected_leaderboard_row)

  def test_to_json_round_trip(self) -> None:
    leaderboard_row = LeaderboardRow(
      "Bot1", LeaderboardPerf(1500, 12, 34, 100, True), RankInfo(4, 1, 50, 10, 3, 1600, DATE_2025_04_01)
    )
    self.assertEqual(LeaderboardRow.from_json(leaderboard_row.to_json()), leaderboard_row)
