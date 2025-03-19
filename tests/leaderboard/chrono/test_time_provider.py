"""Tests for time_provider.py."""

import unittest

from leaderboard.chrono.fake_time_provider import FakeTimeProvider
from src.leaderboard.chrono import time_provider


class TestTimeProviderMethods(unittest.TestCase):
  """Tests for time_provider methods."""

  def test_format_date(self) -> None:
    self.assertEqual(time_provider.format_date(1290415680, time_provider.FORMAT_YYYY_MM_DD), "2010-11-22")


class TestTimeProvider(unittest.TestCase):
  """Tests for TimeProvider."""

  def test_get_current_date_formatted(self) -> None:
    fake_time_provider = FakeTimeProvider()
    fake_time_provider.set_current_time(1743483600)
    self.assertEqual(fake_time_provider.get_current_date_formatted(), "2025-04-01")

  def test_get_current_date_time_formatted(self) -> None:
    fake_time_provider = FakeTimeProvider()
    fake_time_provider.set_current_time(1743483600)
    self.assertEqual(fake_time_provider.get_current_date_time_formatted(), "2025-04-01 05:00:00")
