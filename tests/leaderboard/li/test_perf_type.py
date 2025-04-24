"""Tests for perf_type.py."""

import unittest

from src.leaderboard.li.pert_type import PerfType


class TestPerfType(unittest.TestCase):
  """Tests for PerfType."""

  def test_from_json(self) -> None:
    self.assertEqual(PerfType.from_json("bullet"), PerfType.BULLET)
    self.assertEqual(PerfType.from_json("blitz"), PerfType.BLITZ)
    self.assertEqual(PerfType.from_json("rapid"), PerfType.RAPID)
    self.assertEqual(PerfType.from_json("classical"), PerfType.CLASSICAL)
    self.assertEqual(PerfType.from_json("correspondence"), PerfType.CORRESPONDENCE)
    self.assertEqual(PerfType.from_json("crazyhouse"), PerfType.CRAZYHOUSE)
    self.assertEqual(PerfType.from_json("chess960"), PerfType.CHESS960)
    self.assertEqual(PerfType.from_json("kingOfTheHill"), PerfType.KING_OF_THE_HILL)
    self.assertEqual(PerfType.from_json("threeCheck"), PerfType.THREE_CHECK)
    self.assertEqual(PerfType.from_json("antichess"), PerfType.ANTICHESS)
    self.assertEqual(PerfType.from_json("atomic"), PerfType.ATOMIC)
    self.assertEqual(PerfType.from_json("horde"), PerfType.HORDE)
    self.assertEqual(PerfType.from_json("racingKings"), PerfType.RACING_KINGS)
    self.assertEqual(PerfType.from_json(""), PerfType.UNKNOWN)

  def test_to_string_round_trip(self) -> None:
    for perf_type in PerfType:
      self.assertEqual(PerfType.from_json(perf_type.to_string()), perf_type)

  def test_get_readable_name(self) -> None:
    self.assertEqual(PerfType.BULLET.get_readable_name(), "Bullet")
    self.assertEqual(PerfType.BLITZ.get_readable_name(), "Blitz")
    self.assertEqual(PerfType.RAPID.get_readable_name(), "Rapid")
    self.assertEqual(PerfType.CLASSICAL.get_readable_name(), "Classical")
    self.assertEqual(PerfType.CORRESPONDENCE.get_readable_name(), "Correspondence")
    self.assertEqual(PerfType.CRAZYHOUSE.get_readable_name(), "Crazyhouse")
    self.assertEqual(PerfType.CHESS960.get_readable_name(), "Chess960")
    self.assertEqual(PerfType.KING_OF_THE_HILL.get_readable_name(), "King of the Hill")
    self.assertEqual(PerfType.THREE_CHECK.get_readable_name(), "Three Check")
    self.assertEqual(PerfType.ANTICHESS.get_readable_name(), "Antichess")
    self.assertEqual(PerfType.ATOMIC.get_readable_name(), "Atomic")
    self.assertEqual(PerfType.HORDE.get_readable_name(), "Horde")
    self.assertEqual(PerfType.RACING_KINGS.get_readable_name(), "Racing Kings")
    self.assertEqual(PerfType.UNKNOWN.get_readable_name(), "Unknown")

  def test_all_except_unknown(self) -> None:
    all_except_unknown = list(PerfType.all_except_unknown())
    for perf_type in PerfType:
      if perf_type == PerfType.UNKNOWN:
        self.assertNotIn(perf_type, all_except_unknown)
      else:
        self.assertIn(perf_type, all_except_unknown)
