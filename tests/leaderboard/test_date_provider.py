"""Tests for date_provider.py."""

import unittest

from leaderboard.fake_date_provider import FakeDateProvider
from src.leaderboard import date_provider


class TestDateProviderMethods(unittest.TestCase):
  """Tests for date_provider methods."""

  def test_format_date(self) -> None:
    self.assertEqual(date_provider.format_date(1290415680, date_provider.FORMAT_YYYY_MM_DD), "2010-11-22")


class TestDateProvider(unittest.TestCase):
  """Tests for DateProvider."""

  def test_get_current_date_formatted(self) -> None:
    fake_date_provider = FakeDateProvider()
    fake_date_provider.set_current_time(1743483600)
    self.assertEqual(fake_date_provider.get_current_date_formatted(), "2025-04-01")

  def test_get_current_date_time_formatted(self) -> None:
    fake_date_provider = FakeDateProvider()
    fake_date_provider.set_current_time(1743483600)
    self.assertEqual(fake_date_provider.get_current_date_time_formatted(), "2025-04-01 05:00:00")
