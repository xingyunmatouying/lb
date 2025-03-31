"""Tests for date_formatter.py."""

import unittest

from src.leaderboard.chrono import date_formatter


class TestDateFormatter(unittest.TestCase):
  """Tests for date_formatter functions."""

  def test_format_yyyy_mm_dd(self) -> None:
    self.assertEqual(date_formatter.format_yyyy_mm_dd(1290415680), "2010-11-22")

  def test_format_yyyy_mm_dd_hh_mm_ss(self) -> None:
    self.assertEqual(date_formatter.format_yyyy_mm_dd_hh_mm_ss(1743483600), "2025-04-01 05:00:00")
