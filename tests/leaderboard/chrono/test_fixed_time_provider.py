"""Tests for fixed_time_provider.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider


class TestFixedTimeProvider(unittest.TestCase):
  """Tests for FixedTimeProvider."""

  def test_get_current_time(self) -> None:
    fixed_time_provider = FixedTimeProvider(1743483600)
    self.assertEqual(fixed_time_provider.get_current_time(), 1743483600)
