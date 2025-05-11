"""Tests for file_system.py."""

import unittest

from tests.leaderboard.fs.in_memory_file_system import InMemoryFileSystem


FILE_NAME = "test"
FILE_LINES = "1\n2\n3"


class TestFileSystem(unittest.TestCase):
  """Tests for FileSystem."""

  def test_save_and_load(self) -> None:
    file_system = InMemoryFileSystem()
    file_system.write_file(FILE_NAME, FILE_LINES)
    self.assertEqual(file_system.read_file(FILE_NAME), FILE_LINES)
