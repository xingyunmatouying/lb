"""Tests for leaderboard_generator.py."""

import unittest

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.fs import file_paths
from src.leaderboard.li.pert_type import PerfType
from src.leaderboard.main import leaderboard_generator as leaderboard_generation_functions
from src.leaderboard.main.leaderboard_generator import LeaderboardGenerator
from tests.leaderboard.fs.in_memory_file_system import InMemoryFileSystem
from tests.leaderboard.li.fake_lichess_client import FakeLichessClient
from tests.leaderboard.log.fake_log_writer import FakeLogWriter


class TestLeaderboardGeneratorFunctions(unittest.TestCase):
  """Tests for leaderboard generator functions."""

  def test_increment_generation_number(self) -> None:
    file_system = InMemoryFileSystem()
    leaderboard_generation_functions.increment_generation_number(file_system)
    self.assertEqual(file_system.read_file(file_paths.generation_number_path()), "1")
    leaderboard_generation_functions.increment_generation_number(file_system)
    self.assertEqual(file_system.read_file(file_paths.generation_number_path()), "2")


class TestLeaderboardGenerator(unittest.TestCase):
  """Tests for leaderboard generator."""

  def test_generate_leaderboard(self) -> None:
    file_system = InMemoryFileSystem()
    lichess_client = FakeLichessClient()
    time_provider = FixedTimeProvider(0)
    log_writer = FakeLogWriter()

    lichess_client.set_online_bots("""{ "username": "Bot-1", "perfs": { "bullet": { "rating": 2345, "games": 678 } } }""")

    leaderboard_generator = LeaderboardGenerator(file_system, lichess_client, time_provider, log_writer)
    leaderboard_generator.generate_leaderboards()

    bullet_data = file_system.read_file(file_paths.data_path(PerfType.BULLET))
    if not bullet_data:
      self.fail(f"Missing bullet_data: {bullet_data}")
    self.assertIn("Bot-1", bullet_data)

    bullet_html = file_system.read_file(file_paths.html_path(PerfType.BULLET.to_string()))
    if not bullet_html:
      self.fail(f"Missing bullet_html: {bullet_html}")
    self.assertIn("Bot-1", bullet_html)
