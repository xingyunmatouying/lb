"""Tests for lichess_client.py."""

import unittest

from tests.leaderboard.li.fake_lichess_client import FakeLichessClient


ONLINE_BOT_NDJSON = "{some json}"


class TestLichessClient(unittest.TestCase):
  """Tests for LichessClient."""

  def test_get_online_bots(self) -> None:
    lichess_client = FakeLichessClient()
    lichess_client.set_online_bots(ONLINE_BOT_NDJSON)
    self.assertEqual(lichess_client.get_online_bots(), ONLINE_BOT_NDJSON)
