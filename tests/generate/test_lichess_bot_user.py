"""Tests for lichess_bot_user.py."""

import unittest

from src.generate.lichess_bot_user import BotUser, Perf, PerfType


TEST_BOT_USER_JSON = """
{
  "id": "test_username",
  "username": "Test_Username",
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


class TestPerfType(unittest.TestCase):
  """Tests for PerfType."""

  def test_from_json(self) -> None:
    self.assertEqual(PerfType.from_json("bullet"), PerfType.BULLET)
    self.assertEqual(PerfType.from_json("blitz"), PerfType.BLITZ)
    self.assertEqual(PerfType.from_json("rapid"), PerfType.RAPID)
    self.assertEqual(PerfType.from_json("classical"), PerfType.CLASSICAL)
    self.assertEqual(PerfType.from_json("correspondence"), PerfType.CORRESPONDENCE)
    self.assertEqual(PerfType.from_json("crazyhouse"), PerfType.CRAZYHOUSE)
    self.assertEqual(PerfType.from_json("chess960"), PerfType.CHESS960)
    self.assertEqual(PerfType.from_json("kingOfTheHill"), PerfType.KING_OF_THE_HILL)
    self.assertEqual(PerfType.from_json("threeCheck"), PerfType.THREE_CHECK)
    self.assertEqual(PerfType.from_json("antichess"), PerfType.ANTICHESS)
    self.assertEqual(PerfType.from_json("atomic"), PerfType.ATOMIC)
    self.assertEqual(PerfType.from_json("horde"), PerfType.HORDE)
    self.assertEqual(PerfType.from_json("racingKings"), PerfType.RACING_KINGS)
    self.assertEqual(PerfType.from_json(""), PerfType.UNKNOWN)

  def test_to_string_round_trip(self) -> None:
    for perf_type in PerfType:
      self.assertEqual(PerfType.from_json(perf_type.to_string()), perf_type)

  def test_all_except_unknown(self) -> None:
    all_except_unknown = list(PerfType.all_except_unknown())
    for perf_type in PerfType:
      if perf_type == PerfType.UNKNOWN:
        self.assertNotIn(perf_type, all_except_unknown)
      else:
        self.assertIn(perf_type, all_except_unknown)


class TestLichessClient(unittest.TestCase):
  """Tests for BotUser."""

  def test_from_json(self) -> None:
    bot_user = BotUser.from_json(TEST_BOT_USER_JSON)
    expected_perfs = [
      Perf(PerfType.BULLET, 123, 1450, False),
      Perf(PerfType.BLITZ, 456, 1500, False),
      Perf(PerfType.RAPID, 789, 1550, True),
    ]
    self.assertEqual(bot_user.username, "Test_Username")
    self.assertListEqual(bot_user.perfs, expected_perfs)
