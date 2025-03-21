"""Tests for time_provider.py."""

import unittest

from leaderboard.chrono.fake_time_provider import FakeTimeProvider


class TestTimeProvider(unittest.TestCase):
  """Tests for TimeProvider."""

  def test_get_current_time(self) -> None:
    fake_time_provider = FakeTimeProvider()
    fake_time_provider.set_current_time(1743483600)
    self.assertEqual(fake_time_provider.get_current_time(), 1743483600)
