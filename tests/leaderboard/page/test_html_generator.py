"""Tests for html_generator.py."""

import unittest

from leaderboard.fake_date_provider import FakeDateProvider
from src.leaderboard.leaderboard_data import LeaderboardRow
from src.leaderboard.li.bot_user import PerfType
from src.leaderboard.page.html_generator import LeaderboardHtmlGenerator


class TestHtmlGenerator(unittest.TestCase):
  """Tests for html generator."""

  def test_generate_index(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FakeDateProvider())
    index_html = html_generator.generate_leaderboard_html({})["index"]
    self.assertIn('<a href="index.html" class="active">Home</a>', index_html)

  def test_generate_last_updated(self) -> None:
    date_provider = FakeDateProvider()
    date_provider.set_current_time(1743483600)
    html_generator = LeaderboardHtmlGenerator(date_provider)
    index_html = html_generator.generate_leaderboard_html({})["index"]
    self.assertIn("Last Updated:", index_html)
    self.assertIn("2025-04-01 05:00:00 UTC", index_html)

  def test_generate_bullet(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FakeDateProvider())
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRow.from_json("""{"perf": {"username": "Bot-2"}}"""),
        LeaderboardRow.from_json("""{"perf": {"username": "Bot-1"}}"""),
      ]
    }
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("Bot-2", bullet_html)
    self.assertIn("Bot-1", bullet_html)

  def test_generate_new_bot(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FakeDateProvider())
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"is_new": true}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("🆕", bullet_html)

  def test_generate_positive_rank_delta(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FakeDateProvider())
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"rank_delta": 3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("↑3", bullet_html)
    self.assertIn('class="delta-pos"', bullet_html)

  def test_generate_negative_rank_delta(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FakeDateProvider())
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"rank_delta": -3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("↓3", bullet_html)
    self.assertIn('class="delta-neg"', bullet_html)
