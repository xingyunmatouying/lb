"""Tests for file_system.py."""

import unittest

from leaderboard.in_memory_file_system import InMemoryFileSystem


FILE_NAME = "test"
FILE_LINES = ["1", "2", "3"]


class TestFileSystem(unittest.TestCase):
  """Tests for FileSystem."""

  def test_save_and_load(self) -> None:
    file_system = InMemoryFileSystem()
    file_system.save_file_lines(FILE_NAME, FILE_LINES)
    self.assertListEqual(file_system.load_file_lines(FILE_NAME), FILE_LINES)
