"""Generate lichess bot leaderboards for each time control and variant.

Process for generating the leaderboards:
 - Call the lichess `get online bots` API (https://lichess.org/api/bot/online)
 - Parse the response into collection of bots and ratings
 - Create leaderboards which are fun to look at
"""

import logging
import time

from src.leaderboard.chrono.real_time_provider import RealTimeProvider
from src.leaderboard.data import data_generator
from src.leaderboard.data.data_generator import LeaderboardDataGenerator
from src.leaderboard.fs.real_file_system import RealFileSystem
from src.leaderboard.li.real_lichess_client import RealLichessClient
from src.leaderboard.page.html_generator import LeaderboardHtmlGenerator


def create_logger() -> logging.Logger:
  """Initialize and return a logger."""
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)
  stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
  logger.addHandler(stream_handler)
  return logger


if __name__ == "__main__":
  # Start timer
  start_time = time.time()

  # Setup logging
  logger = create_logger()
  logger.info("Generating leaderboard...")

  # Instantiate dependencies
  file_system = RealFileSystem()
  lichess_client = RealLichessClient()
  time_provider = RealTimeProvider()

  # Generate leaderboard
  leaderboard_data_generator = LeaderboardDataGenerator(file_system, lichess_client, time_provider)
  ranked_rows_by_perf_type = leaderboard_data_generator.generate_leaderboard_data()

  # Save the leaderboard data
  for perf_type, rows in ranked_rows_by_perf_type.items():
    file_system.save_file_lines(data_generator.get_leaderboard_data_file_name(perf_type), [row.to_json() for row in rows])

  leaderboard_html_generator = LeaderboardHtmlGenerator(time_provider)
  html_by_name = leaderboard_html_generator.generate_leaderboard_html(ranked_rows_by_perf_type)

  # save the leaderboard html
  for name, html in html_by_name.items():
    file_system.save_file_lines(f"leaderboard_html/{name}.html", [html])

  # Print time elapsed
  time_elapsed = time.time() - start_time
  logger.info(f"Finished in {time_elapsed:.2f}s")
