"""Leaderboard generator."""

import json
import time

from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data.data_generator import DataGenerator
from src.leaderboard.fs import file_paths
from src.leaderboard.fs.file_system import FileSystem
from src.leaderboard.li.lichess_client import LichessClient
from src.leaderboard.log.log_writer import LogWriter
from src.leaderboard.page.html_generator import HtmlGenerator


def increment_generation_number(file_system: FileSystem) -> None:
  """Increments the value generation number number file."""
  value_str = file_system.read_file(file_paths.generation_number_path())
  value = int(value_str) if value_str else 0
  file_system.write_file(file_paths.generation_number_path(), str(value + 1))


class LeaderboardGenerator:
  """Generator of leaderboards."""

  def __init__(
    self, file_system: FileSystem, lichess_client: LichessClient, time_provider: TimeProvider, log_writer: LogWriter
  ) -> None:
    """Initialize a new generator."""
    self.file_system = file_system
    self.lichess_client = lichess_client
    self.time_provider = time_provider
    self.log_writer = log_writer

  def generate_leaderboards(self) -> None:
    """Generate the leaderboards."""
    # Start timer
    start_time = time.time()
    self.log_writer.info("Generating leaderboards...")

    # Generate leaderboard data
    data_generator = DataGenerator(self.file_system, self.lichess_client, self.time_provider)
    leaderboard_data = data_generator.generate_leaderboard_data()

    # Save the leaderboard data
    bot_profile_dicts = [bot_profile.as_dict() for bot_profile in leaderboard_data.get_bot_profiles_sorted()]
    self.file_system.write_file(file_paths.bot_profiles_path(), json.dumps(bot_profile_dicts, indent=2))
    for perf_type, rows in leaderboard_data.get_ranked_rows_sorted().items():
      row_dicts = [row.as_dict() for row in rows]
      self.file_system.write_file(file_paths.data_path(perf_type), json.dumps(row_dicts, indent=2))

    # Generate leaderboard html
    html_generator = HtmlGenerator(self.time_provider)
    html_by_name = html_generator.generate_leaderboard_html(leaderboard_data)

    # Save the leaderboard html
    for name, html in html_by_name.items():
      self.file_system.write_file(file_paths.html_path(name), html)

    # Make note of how many times we have generated the leaderboards
    increment_generation_number(self.file_system)

    # Print time elapsed
    time_elapsed = time.time() - start_time
    self.log_writer.info("Finished in %.2fs", time_elapsed)
