"""Tests for bot_user.py."""

import unittest

from src.leaderboard.li.bot_user import BotUser, Perf
from src.leaderboard.li.pert_type import PerfType


BOT_USER_JSON = """
{
  "id": "test_username",
  "username": "Test_Username",
  "flair": "symbol",
  "profile": {
    "flag": "_earth"
  },
  "createdAt": 1000000000000,
  "seenAt": 2000000000000,
  "patron": true,
  "perfs": {
    "bullet": {
        "games": 123,
        "rating": 1450
    },
    "blitz": {
        "games": 456,
        "rating": 1500
    },
    "rapid": {
        "games": 789,
        "rating": 1550,
        "prov": true
    }
  }
}
"""


class TestPerf(unittest.TestCase):
  """Tests for Perf."""

  def test_from_json_dict(self) -> None:
    json_key = "bullet"
    json_value = {"games": 15, "rating": 2800, "rd": 200, "prog": 700, "prov": True}
    self.assertEqual(Perf.from_json_dict(json_key, json_value), Perf(PerfType.BULLET, 15, 2800, 200, 700, True))


class TestBotUser(unittest.TestCase):
  """Tests for BotUser."""

  def test_from_json(self) -> None:
    bot_user = BotUser.from_json(BOT_USER_JSON)
    expected_perfs = [
      Perf(PerfType.BULLET, 123, 1450, 0, 0, False),
      Perf(PerfType.BLITZ, 456, 1500, 0, 0, False),
      Perf(PerfType.RAPID, 789, 1550, 0, 0, True),
    ]
    self.assertEqual(bot_user.username, "Test_Username")
    self.assertEqual(bot_user.flair, "symbol")
    self.assertEqual(bot_user.flag, "_earth")
    self.assertEqual(bot_user.created_at, 1000000000)
    self.assertEqual(bot_user.seen_at, 2000000000)
    self.assertTrue(bot_user.patron)
    self.assertFalse(bot_user.tos_violation)
    self.assertListEqual(bot_user.perfs, expected_perfs)
