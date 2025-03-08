"""Tests for html_generator.py."""

import unittest

from src.generate.html_generator import LeaderboardHtmlGenerator
from src.generate.leaderboard_data import LeaderboardRow
from src.generate.lichess_bot_user import PerfType


class TestHtmlGenerator(unittest.TestCase):
  """Tests for html generator."""

  def test_generate_leaderboard_html_index(self) -> None:
    html_generator = LeaderboardHtmlGenerator()
    html_by_file_name = html_generator.generate_leaderboard_html({})
    index_html = html_by_file_name["index"]
    self.assertIn('<a href="index.html" class="active">Home</a>', index_html)

  def test_generate_leaderboard_html_bullet(self) -> None:
    html_generator = LeaderboardHtmlGenerator()
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRow.from_psv("Bot-2|||3000|0|0|1000|2022-04-01|2025-04-01|False|False|1|1|100|1|3000|False"),
        LeaderboardRow.from_psv("Bot-1|flair|_earth|2950|42|-50|1100|2024-04-01|2025-04-01|True|False|2|-1|-50|1|3000|False"),
      ]
    }
    html_by_file_name = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)
    bullet_html = html_by_file_name["bullet"]
    self.assertIn("Bot-2", bullet_html)
    self.assertIn("Bot-1", bullet_html)
