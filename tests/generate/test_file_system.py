"""Tests for file_system.py."""

import unittest

from generate.in_memory_file_system import InMemoryFileSystem


TEST_FILE_NAME = "test"
TEST_FILE_LINES = ["1", "2", "3"]


class TestFileSystem(unittest.TestCase):
  """Tests for FileSystem."""

  def test_save_and_load(self) -> None:
    file_system = InMemoryFileSystem()
    file_system.save_file_lines(TEST_FILE_NAME, TEST_FILE_LINES)
    self.assertListEqual(file_system.load_file_lines(TEST_FILE_NAME), TEST_FILE_LINES)
