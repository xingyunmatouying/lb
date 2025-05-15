"""Tests for html_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data.data_generator import LeaderboardDataResult
from src.leaderboard.data.leaderboard_objects import BotProfile, LeaderboardPerf, LeaderboardRow, RankInfo
from src.leaderboard.li.pert_type import PerfType
from src.leaderboard.page.html_generator import (
  Flag,
  HtmlGenerator,
  HtmlLeaderboardRow,
  LeaderboardDelta,
  MainFrame,
  OnlineStatus,
)
from tests.leaderboard.chrono import epoch_seconds


DEFAULT_BOT_PROFILES_BY_NAME = {
  "Bot-1": BotProfile.from_dict({"name": "Bot-1"}),
  "Bot-2": BotProfile.from_dict({"name": "Bot-2"}),
}

DATE_2024_10_31 = epoch_seconds.from_date(2024, 10, 31)
DATE_2025_03_30 = epoch_seconds.from_date(2025, 3, 30)
DATE_2025_04_01 = epoch_seconds.from_date(2025, 4, 1)


def create_leaderboard_row(name: str, rank: int = 1, delta_rank: int = 0, delta_rating: int = 0) -> LeaderboardRow:
  """Create a LeaderboardRow with several default values set."""
  return LeaderboardRow(name, LeaderboardPerf(0, 0, 0, 0, False), RankInfo(rank, delta_rank, delta_rating, 0, 0, 0, 0))


class TestMainFrame(unittest.TestCase):
  """Tests for MainFrame."""

  def test_from_perf_type_bullet(self) -> None:
    main_frame = MainFrame.from_perf_type(PerfType.BULLET, DATE_2025_04_01)
    self.assertEqual(main_frame.title, "Bullet")

  def test_from_perf_type_none(self) -> None:
    main_frame = MainFrame.from_perf_type(None, DATE_2025_04_01)
    self.assertEqual(main_frame.title, "Lichess Bot Leaderboard")


class TestLeaderboardDelta(unittest.TestCase):
  """Tests for LeaderboardDelta."""

  def for_delta(self) -> None:
    self.assertEqual(LeaderboardDelta.for_delta(1), LeaderboardDelta("+1", LeaderboardDelta.DELTA_POS_CLASS))
    self.assertEqual(LeaderboardDelta.for_delta(-1), LeaderboardDelta("-1", LeaderboardDelta.DELTA_NEG_CLASS))
    self.assertEqual(LeaderboardDelta.for_delta(0), LeaderboardDelta("", ""))

  def test_for_delta_rank(self) -> None:
    self.assertEqual(LeaderboardDelta.for_delta_rank(2, -2, True), LeaderboardDelta("🆕", ""))
    self.assertEqual(LeaderboardDelta.for_delta_rank(2, -2, False), LeaderboardDelta("🔙", ""))
    self.assertEqual(LeaderboardDelta.for_delta_rank(2, 1, False), LeaderboardDelta("↑1", LeaderboardDelta.DELTA_POS_CLASS))
    self.assertEqual(LeaderboardDelta.for_delta_rank(2, -1, False), LeaderboardDelta("↓1", LeaderboardDelta.DELTA_NEG_CLASS))
    self.assertEqual(LeaderboardDelta.for_delta_rank(2, 0, False), LeaderboardDelta("", ""))


class TestOnlineStatus(unittest.TestCase):
  """Tests for OnlineStatus."""

  def test_create_from(self) -> None:
    expected_online_patron_status = OnlineStatus(OnlineStatus.PATRON_INDICATOR, OnlineStatus.BOT_ONLINE_CLASS)
    self.assertEqual(OnlineStatus.create_from(True, True), expected_online_patron_status)
    expected_offline_default_status = OnlineStatus(OnlineStatus.DEFAULT_INDICATOR, OnlineStatus.BOT_OFFLINE_CLASS)
    self.assertEqual(OnlineStatus.create_from(False, False), expected_offline_default_status)


class TestFlag(unittest.TestCase):
  """Tests for Flag."""

  def test_from_string(self) -> None:
    self.assertEqual(Flag.from_string("HM"), Flag("🇭🇲", ""))
    self.assertEqual(Flag.from_string("_earth"), Flag("", "earth-flag"))


class TestHtmlLeaderboardRow(unittest.TestCase):
  """Tests for HtmlLeaderboardRow."""

  def test_from_leaderboard_row(self) -> None:
    bot_profile = BotProfile("Bot-1", "flair", "HM", DATE_2024_10_31, DATE_2025_04_01, True, False, False, True)
    perf = LeaderboardPerf(3000, 45, 12, 1000, False)
    rank_info = RankInfo(2, 1, -5, 10, 3100, 1, DATE_2025_03_30)
    leaderboard_row = LeaderboardRow("Bot-1", perf, rank_info)
    expected_html_row = HtmlLeaderboardRow(
      "🥈",
      2,
      LeaderboardDelta("↑1", LeaderboardDelta.DELTA_POS_CLASS),
      OnlineStatus(OnlineStatus.PATRON_INDICATOR, OnlineStatus.BOT_ONLINE_CLASS),
      "Bot-1",
      Flag("🇭🇲", ""),
      3000,
      LeaderboardDelta("-5", LeaderboardDelta.DELTA_NEG_CLASS),
      45,
      1000,
      LeaderboardDelta("+10", LeaderboardDelta.DELTA_POS_CLASS),
      "5mo",
      "",
    )
    self.assertEqual(HtmlLeaderboardRow.from_leaderboard_row(leaderboard_row, bot_profile, DATE_2025_04_01), expected_html_row)


class TestHtmlGenerator(unittest.TestCase):
  """Tests for HtmlGenerator."""

  def test_generate_index(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1"), create_leaderboard_row("Bot-2")]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    index_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["index"]
    self.assertIn('<a href="index.html" class="active">Home</a>', index_html)
    self.assertIn("Bullet", index_html)
    self.assertIn("Bot-1", index_html)
    self.assertIn("Bot-2", index_html)
    self.assertIn('name="description" content="Automatically updated', index_html)
    self.assertIn('name="keywords" content="Lichess bot leaderboard,', index_html)

  def test_generate_last_updated(self) -> None:
    time_provider = FixedTimeProvider(1743483600)
    html_generator = HtmlGenerator(time_provider)
    index_html = html_generator.generate_leaderboard_html(LeaderboardDataResult.create_result({}, {}))["index"]
    self.assertIn("Last Updated:", index_html)
    self.assertIn("2025-04-01 05:00:00 UTC", index_html)

  def test_generate_bullet(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1"), create_leaderboard_row("Bot-2")]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("<h1>Bullet</h1>", bullet_html)
    self.assertIn("Bot-1", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-1", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-1/perf/bullet", bullet_html)
    self.assertIn("Bot-2", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-2", bullet_html)
    self.assertIn("https://lichess.org/@/Bot-2/perf/bullet", bullet_html)

  def test_generate_no_ineligible(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1", rank=0)]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertNotIn("Bot-1", bullet_html)

  def test_generate_new_bot(self) -> None:
    bot_profiles_by_name = {"Bot-1": BotProfile("Bot-1", "", "", 0, 0, False, False, True, True)}
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1")]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(bot_profiles_by_name, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("🆕", bullet_html)

  def test_generate_positive_delta_rank(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1", delta_rank=3)]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("↑3", bullet_html)
    self.assertIn(f'class="col-delta-rank {LeaderboardDelta.DELTA_POS_CLASS}"', bullet_html)

  def test_generate_negative_delta_rank(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1", delta_rank=-3)]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("↓3", bullet_html)
    self.assertIn(f'class="col-delta-rank {LeaderboardDelta.DELTA_NEG_CLASS}"', bullet_html)

  def test_generate_positive_delta_rating(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1", delta_rating=3)]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("+3", bullet_html)
    self.assertIn(f'class="col-delta-rating {LeaderboardDelta.DELTA_POS_CLASS}"', bullet_html)

  def test_generate_negative_delta_rating(self) -> None:
    ranked_rows_by_perf_type = {PerfType.BULLET: [create_leaderboard_row("Bot-1", delta_rating=-3)]}
    html_generator = HtmlGenerator(FixedTimeProvider(0))
    bullet_html = html_generator.generate_leaderboard_html(
      LeaderboardDataResult.create_result(DEFAULT_BOT_PROFILES_BY_NAME, ranked_rows_by_perf_type)
    )["bullet"]
    self.assertIn("-3", bullet_html)
    self.assertIn(f'class="col-delta-rating {LeaderboardDelta.DELTA_NEG_CLASS}"', bullet_html)
