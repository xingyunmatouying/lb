"""Tests for meta_tags.py."""

import unittest

from src.leaderboard.li.pert_type import PerfType
from src.leaderboard.page import meta_tags


class TestMetaTags(unittest.TestCase):
  """Tests for meta_tags functions."""

  def test_get_description_bullet(self) -> None:
    self.assertIn("Automatically updated Lichess bot Bullet leaderboard.", meta_tags.get_description(PerfType.BULLET))

  def test_get_description_index(self) -> None:
    self.assertIn("Automatically updated Lichess bot leaderboards.", meta_tags.get_description(None))

  def test_get_keywords_bullet(self) -> None:
    self.assertIn("Bullet bot leaderboard, best bot at Bullet", meta_tags.get_keywords(PerfType.BULLET))

  def test_get_keywords_index(self) -> None:
    index_keywords = meta_tags.get_keywords(None)
    self.assertIn("Lichess bot leaderboard, best bot on Lichess", index_keywords)
    self.assertIn("Bullet leaderboard", index_keywords)
    self.assertIn("Blitz leaderboard", index_keywords)
