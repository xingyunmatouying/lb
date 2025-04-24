"""Tests for default_remover.py."""

import unittest

from src.leaderboard.data import default_remover


class TestDefaultRemoverFunctions(unittest.TestCase):
  """Tests for default_remover functions."""

  def test_to_dict_without_defaults(self) -> None:
    sparse_dict = {
      "key1": 0,
      "key2": "",
      "key3": False,
      "key4": {"key5": 0, "key6": {"key7": False}},
      "key8": {"key9": True},
      "key10": 10,
    }
    expected_dict = {
      "key8": {
        "key9": True,
      },
      "key10": 10,
    }
    self.assertEqual(default_remover.to_dict_without_defaults(sparse_dict), expected_dict)
