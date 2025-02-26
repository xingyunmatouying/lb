"""Tests for lichess_client.py."""

import unittest

from src.generate import lichess_client
from src.generate.online_bot_user import OnlineBotUser


TEST_ONLINE_BOT_USER = OnlineBotUser("test", [])


class MockLichessClient(lichess_client.LichessClient):
  def get_online_bots(self) -> list[OnlineBotUser]:
    return [TEST_ONLINE_BOT_USER]


class TestLichessClient(unittest.TestCase):
  def test_get_online_bots_with_mock_client_returns_mock_response(self) -> None:
    lichess_client = MockLichessClient()
    self.assertEqual(lichess_client.get_online_bots(), [TEST_ONLINE_BOT_USER])
