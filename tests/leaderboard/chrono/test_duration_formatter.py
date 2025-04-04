"""Tests for duration_formatter.py."""

import unittest

from src.leaderboard.chrono import duration_formatter
from tests.leaderboard.chrono import epoch_seconds


DATE_2024_03_02 = epoch_seconds.from_date(2024, 3, 2)
DATE_2024_04_02 = epoch_seconds.from_date(2024, 4, 2)
DATE_2024_05_01 = epoch_seconds.from_date(2024, 5, 1)

DATE_2025_03_02 = epoch_seconds.from_date(2025, 3, 2)
DATE_2025_04_01 = epoch_seconds.from_date(2025, 4, 1)


class TestDurationFormatter(unittest.TestCase):
  """Tests for duration_formatter functions."""

  def test_format_age(self) -> None:
    self.assertEqual(duration_formatter.format_age(DATE_2024_05_01, DATE_2025_04_01), "11mo")
    self.assertEqual(duration_formatter.format_age(DATE_2024_04_02, DATE_2025_04_01), "11mo")
    self.assertEqual(duration_formatter.format_age(DATE_2024_03_02, DATE_2025_04_01), "1y 0mo")
    self.assertEqual(duration_formatter.format_age(DATE_2025_03_02, DATE_2025_04_01), "<1mo")
    self.assertEqual(duration_formatter.format_age(DATE_2025_04_01, DATE_2025_03_02), "<1mo")

  def test_format_age_birthday(self) -> None:
    self.assertEqual(duration_formatter.format_age(DATE_2024_03_02, DATE_2025_03_02), "🎂 1y 🎂")
