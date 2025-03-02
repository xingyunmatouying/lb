"""Generate lichess bot leaderboards for each time control and variant.

Process for generating the leaderboards:
 - Call the lichess `get online bots` API (https://lichess.org/api/bot/online)
 - Parse the response into collection of bots and ratings
 - Create leaderboards which are fun to look at
"""

import logging
import time

from src.generate.generator import LeaderboardGenerator
from src.generate.real_date_provider import RealDateProvider
from src.generate.real_file_system import RealFileSystem
from src.generate.real_lichess_client import RealLichessClient


if __name__ == "__main__":
  # Setup logging
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)
  formatter = logging.Formatter("%(levelname)s: %(message)s")
  stream_handler.setFormatter(formatter)  # using the formatter.
  logger.addHandler(stream_handler)
  logger.info("Generating leaderboard...")

  # Instantiate dependencies
  file_system = RealFileSystem()
  lichess_client = RealLichessClient()
  date_provider = RealDateProvider()

  # Generate leaderboard
  start_time = time.time()
  leaderboard_generator = LeaderboardGenerator(file_system, lichess_client, date_provider)
  leaderboard_generator.generate_all_leaderboards()
  time_elapsed_ms = (time.time() - start_time) * 1000

  # Print time elapsed
  logger.info(f"Generation completed in {time_elapsed_ms:.2f}ms")
