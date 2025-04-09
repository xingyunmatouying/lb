"""Tests for html_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data.data_generator import GenerateDataResult
from src.leaderboard.data.leaderboard_row import BotProfile, LeaderboardRowLite
from src.leaderboard.li.pert_type import PerfType
from src.leaderboard.page.html_generator import HtmlGenerator, LeaderboardDelta, OnlineStatus


class TestLeaderboardDelta(unittest.TestCase):
  """Tests for LeaderboardDelta."""

  def test_for_delta_rank(self) -> None:
    self.assertEqual(LeaderboardDelta.for_delta_rank(1, False), LeaderboardDelta("↑1", "delta-pos"))
    self.assertEqual(LeaderboardDelta.for_delta_rank(-1, False), LeaderboardDelta("↓1", "delta-neg"))
    self.assertEqual(LeaderboardDelta.for_delta_rank(0, False), LeaderboardDelta("", ""))
    self.assertEqual(LeaderboardDelta.for_delta_rank(0, True), LeaderboardDelta("🆕", ""))

  def for_delta_rating(self) -> None:
    self.assertEqual(LeaderboardDelta.for_delta_rating(1), LeaderboardDelta("(+1)", "delta-pos"))
    self.assertEqual(LeaderboardDelta.for_delta_rating(-1), LeaderboardDelta("(-1)", "delta-neg"))
    self.assertEqual(LeaderboardDelta.for_delta_rating(0), LeaderboardDelta("", ""))


class TestOnlineStatus(unittest.TestCase):
  """Tests for OnlineStatus."""

  def test_create_from(self) -> None:
    self.assertEqual(OnlineStatus.create_from(True, True), OnlineStatus("★", "bot-online"))
    self.assertEqual(OnlineStatus.create_from(False, False), OnlineStatus("●", "bot-offline"))


class TestHtmlGenerator(unittest.TestCase):
  """Tests for HtmlGenerator."""

  def test_generate_index(self) -> None:
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    index_html = html_generator.generate_leaderboard_html(GenerateDataResult.create_result({}, {}))["index"]
    self.assertIn('<a href="index.html" class="active">Home</a>', index_html)

  def test_generate_last_updated(self) -> None:
    time_provider = FixedTimeProvider(1743483600)
    html_generator = HtmlGenerator(time_provider)
    index_html = html_generator.generate_leaderboard_html(GenerateDataResult.create_result({}, {}))["index"]
    self.assertIn("Last Updated:", index_html)
    self.assertIn("2025-04-01 05:00:00 UTC", index_html)

  def test_generate_bullet(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_2_profile = BotProfile.from_json('{"username": "Bot-2"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile, "Bot-2": bot_2_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1"}').to_leaderboard_row(bot_1_profile),
        LeaderboardRowLite.from_json('{"username": "Bot-2"}').to_leaderboard_row(bot_2_profile),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("<h1>Bullet</h1>", bullet_html)
    self.assertIn("Bot-1", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-1", bullet_html)
    self.assertIn("Bot-2", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-2", bullet_html)

  def test_generate_new_bot(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1", "rank_info": {"is_new": true}}').to_leaderboard_row(bot_1_profile),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("🆕", bullet_html)

  def test_generate_positive_delta_rank(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1", "rank_info": {"delta_rank": 3}}').to_leaderboard_row(
          bot_1_profile
        ),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("↑3", bullet_html)
    self.assertIn('class="col-delta-rank delta-pos"', bullet_html)

  def test_generate_negative_delta_rank(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1", "rank_info": {"delta_rank": -3}}').to_leaderboard_row(
          bot_1_profile
        ),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("↓3", bullet_html)
    self.assertIn('class="col-delta-rank delta-neg"', bullet_html)

  def test_generate_positive_delta_rating(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1", "rank_info": {"delta_rating": 3}}').to_leaderboard_row(
          bot_1_profile
        ),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("(+3)", bullet_html)
    self.assertIn('class="col-delta-rating delta-pos"', bullet_html)

  def test_generate_negative_delta_rating(self) -> None:
    bot_1_profile = BotProfile.from_json('{"username": "Bot-1"}')
    bot_profiles_by_name = {"Bot-1": bot_1_profile}
    ranked_rows_by_perf_type = {
      PerfType.BULLET: [
        LeaderboardRowLite.from_json('{"username": "Bot-1", "rank_info": {"delta_rating": -3}}').to_leaderboard_row(
          bot_1_profile
        ),
      ]
    }
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      GenerateDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("(-3)", bullet_html)
    self.assertIn('class="col-delta-rating delta-neg"', bullet_html)
