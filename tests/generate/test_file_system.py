"""Tests for file_system.py."""

import unittest

from src.generate.file_system import FileSystem


TEST_FILE_NAME = "test"
TEST_FILE_LINES = ["1", "2", "3"]
TEST_FILE_SYSTEM = {TEST_FILE_NAME: TEST_FILE_LINES}


class FakeFileSystem(FileSystem):
  def load_file_lines(self, file_name: str) -> list[str]:
    return TEST_FILE_SYSTEM[file_name]


class TestFileSystem(unittest.TestCase):
  def test_load_file_lines_returns_list(self) -> None:
    file_system = FakeFileSystem()
    self.assertEqual(file_system.load_file_lines(TEST_FILE_NAME), TEST_FILE_LINES)
