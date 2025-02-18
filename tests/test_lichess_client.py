"""
Tests for lichess_client.py
"""

import unittest

from src.generate import lichess_client


class MockLichessClient(lichess_client.LichessClient):
  def get_online_bots(self):
    return "test"


class TestLichessClient(unittest.TestCase):
  def test_get_online_bots_with_mock_client_returns_mock_response(self):
    lichess_client = MockLichessClient()
    self.assertEqual(lichess_client.get_online_bots(), "test")
