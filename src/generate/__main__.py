"""Generate lichess bot leaderboards for each time control and variant.

Process for generating the leaderboards:
 - Call the lichess `get online bots` API (https://lichess.org/api/bot/online)
 - Parse the response into collection of bots and ratings
 - Create leaderboards which are fun to look at
"""

import logging
import time

from src.generate.leaderboard_generator import LeaderboardDataGenerator
from src.generate.real_date_provider import RealDateProvider
from src.generate.real_file_system import RealFileSystem
from src.generate.real_lichess_client import RealLichessClient


if __name__ == "__main__":
  # Start timer
  start_time = time.time()

  # Setup logging
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)
  stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
  logger.addHandler(stream_handler)
  logger.info("Generating leaderboard...")

  # Instantiate dependencies
  file_system = RealFileSystem()
  lichess_client = RealLichessClient()
  date_provider = RealDateProvider()

  # Generate leaderboard
  leaderboard_data_generator = LeaderboardDataGenerator(file_system, lichess_client, date_provider)
  leaderboard_data_generator.generate_leaderboard_data()

  # Print time elapsed
  time_elapsed = time.time() - start_time
  logger.info(f"Finished in {time_elapsed:.2f}s")
