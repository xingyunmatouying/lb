"""Leaderboard generator."""

import time

from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data import data_generator
from src.leaderboard.data.data_generator import DataGenerator
from src.leaderboard.fs.file_system import FileSystem
from src.leaderboard.li.lichess_client import LichessClient
from src.leaderboard.log.log_writer import LogWriter
from src.leaderboard.page.html_generator import LeaderboardHtmlGenerator


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

    self.log_writer.info("Generating leaderboard...")

    # Generate leaderboard
    leaderboard_data_generator = DataGenerator(self.file_system, self.lichess_client, self.time_provider)
    ranked_rows_by_perf_type = leaderboard_data_generator.generate_leaderboard_data()

    # Save the leaderboard data
    for perf_type, rows in ranked_rows_by_perf_type.items():
      self.file_system.save_file_lines(
        data_generator.get_leaderboard_data_file_name(perf_type), [row.to_json() for row in rows]
      )

    leaderboard_html_generator = LeaderboardHtmlGenerator(self.time_provider)
    html_by_name = leaderboard_html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)

    # save the leaderboard html
    for name, html in html_by_name.items():
      self.file_system.save_file_lines(f"leaderboard_html/{name}.html", [html])

    # Print time elapsed
    time_elapsed = time.time() - start_time
    self.log_writer.info("Finished in %.2fs", time_elapsed)
