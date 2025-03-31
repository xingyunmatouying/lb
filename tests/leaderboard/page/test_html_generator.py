"""Tests for html_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data.leaderboard_row import LeaderboardRow
from src.leaderboard.li.bot_user import PerfType
from src.leaderboard.page.html_generator import LeaderboardHtmlGenerator


class TestHtmlGenerator(unittest.TestCase):
  """Tests for html generator."""

  def test_generate_index(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    index_html = html_generator.generate_leaderboard_html({})["index"]
    self.assertIn('<a href="index.html" class="active">Home</a>', index_html)

  def test_generate_last_updated(self) -> None:
    time_provider = FixedTimeProvider(1743483600)
    html_generator = LeaderboardHtmlGenerator(time_provider)
    index_html = html_generator.generate_leaderboard_html({})["index"]
    self.assertIn("Last Updated:", index_html)
    self.assertIn("2025-04-01 05:00:00 UTC", index_html)

  def test_generate_bullet(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRow.from_json("""{"bot_info": {"profile": {"username": "Bot-2"}}}"""),
        LeaderboardRow.from_json("""{"bot_info": {"profile": {"username": "Bot-1"}}}"""),
      ]
    }
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("Bot-2", bullet_html)
    self.assertIn("Bot-1", bullet_html)

  def test_generate_new_bot(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"is_new": true}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("🆕", bullet_html)

  def test_generate_positive_delta_rank(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"delta_rank": 3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("↑3", bullet_html)
    self.assertIn('class="col-delta-rank delta-pos"', bullet_html)

  def test_generate_negative_delta_rank(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"delta_rank": -3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("↓3", bullet_html)
    self.assertIn('class="col-delta-rank delta-neg"', bullet_html)

  def test_generate_positive_delta_rating(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"delta_rating": 3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("(+3)", bullet_html)
    self.assertIn('class="col-delta-rating delta-pos"', bullet_html)

  def test_generate_negative_delta_rating(self) -> None:
    html_generator = LeaderboardHtmlGenerator(FixedTimeProvider(0))
    ranked_rows_by_perf_type = {PerfType.BULLET: [LeaderboardRow.from_json('{"delta_rating": -3}')]}
    bullet_html = html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)["bullet"]
    self.assertIn("(-3)", bullet_html)
    self.assertIn('class="col-delta-rating delta-neg"', bullet_html)
