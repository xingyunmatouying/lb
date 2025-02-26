"""Tests for lichess_client.py."""

import unittest

from src.generate import lichess_client


TEST_ONLINE_BOT_USER = "{some json}"


class MockLichessClient(lichess_client.LichessClient):
  def get_online_bots(self) -> str:
    return TEST_ONLINE_BOT_USER


class TestLichessClient(unittest.TestCase):
  def test_get_online_bots_with_mock_client_returns_mock_response(self) -> None:
    lichess_client = MockLichessClient()
    self.assertEqual(lichess_client.get_online_bots(), TEST_ONLINE_BOT_USER)
