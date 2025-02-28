"""Tests for lichess_client.py."""

import unittest

from src.generate.lichess_client import LichessClient


TEST_ONLINE_BOT_USER = "{some json}"


class FakeLichessClient(LichessClient):
  """A fake implementation of LichessClient."""

  def get_online_bots(self) -> str:
    return TEST_ONLINE_BOT_USER


class TestLichessClient(unittest.TestCase):
  """Tests for LichessClient."""

  def test_get_online_bots(self) -> None:
    lichess_client = FakeLichessClient()
    self.assertEqual(lichess_client.get_online_bots(), TEST_ONLINE_BOT_USER)
