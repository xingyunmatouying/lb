"""Tests for leaderboard_generator.py."""

import unittest

from leaderboard.fs.in_memory_file_system import InMemoryFileSystem
from leaderboard.li.fake_lichess_client import FakeLichessClient
from leaderboard.log.fake_log_writer import FakeLogWriter
from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.data import data_generator
from src.leaderboard.li.bot_user import PerfType
from src.leaderboard.main.leaderboard_generator import LeaderboardGenerator


class TestLeaderboardGenerator(unittest.TestCase):
  """Tests for leaderboard generator."""

  def test_generate_leaderboard(self) -> None:
    file_system = InMemoryFileSystem()
    lichess_client = FakeLichessClient()
    time_provider = FixedTimeProvider(0)
    log_writer = FakeLogWriter()

    lichess_client.set_online_bots("""{ "username": "Bot-1", "perfs": { "bullet": { "rating": 2345 } } }""")

    leaderboard_generator = LeaderboardGenerator(file_system, lichess_client, time_provider, log_writer)
    leaderboard_generator.generate_leaderboards()

    bullet_data = file_system.load_file_lines(data_generator.get_leaderboard_data_file_name(PerfType.BULLET))
    self.assertIn("Bot-1", bullet_data[0])

    bullet_html = file_system.load_file_lines(f"leaderboard_html/{PerfType.BULLET.to_string()}.html")
    self.assertIn("Bot-1", bullet_html[0])
