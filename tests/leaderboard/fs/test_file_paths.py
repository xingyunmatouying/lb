"""Tests for file_paths.py."""

import unittest

from src.leaderboard.fs import file_paths
from src.leaderboard.li.pert_type import PerfType


class TestFileFilePaths(unittest.TestCase):
  """Tests for file_paths."""

  def test_data_path(self) -> None:
    self.assertEqual(file_paths.data_path(PerfType.BULLET), "leaderboard_data/bullet.ndjson")

  def test_html_path(self) -> None:
    self.assertEqual(file_paths.html_path("index"), "leaderboard_html/index.html")
