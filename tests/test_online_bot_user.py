"""Tests for online_bot_user.py."""

import unittest

from src.generate import online_bot_user
from src.generate.online_bot_user import Perf


TEST_ONLINE_BOT_USER_JSON = """
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


class TestLichessClient(unittest.TestCase):
  def test_from_json_parses_username(self) -> None:
    bot_user = online_bot_user.from_json(TEST_ONLINE_BOT_USER_JSON)
    self.assertEqual(bot_user.username, "Test_Username")

  def test_from_json_parses_perfs(self) -> None:
    bot_user = online_bot_user.from_json(TEST_ONLINE_BOT_USER_JSON)
    expected_perfs = [
      Perf("bullet", 123, 1450, False),
      Perf("blitz", 456, 1500, False),
      Perf("rapid", 789, 1550, True),
    ]
    self.assertEqual(bot_user.perfs, expected_perfs)
