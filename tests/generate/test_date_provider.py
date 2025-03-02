"""Tests for date_provider.py."""

import unittest

from src.generate import date_provider

from generate.fake_date_provider import FakeDateProvider


class TestDateProviderMethods(unittest.TestCase):
  """Tests for date_provider methods."""

  def test_format_date(self) -> None:
    self.assertEqual(date_provider.format_date(1290415680000), "2010-11-22")


class TestDateProvider(unittest.TestCase):
  """Tests for DateProvider."""

  def test_get_current_date(self) -> None:
    fake_date_provider = FakeDateProvider()
    fake_date_provider.set_current_date("2025-04-01")
    self.assertEqual(fake_date_provider.get_current_date(), "2025-04-01")
