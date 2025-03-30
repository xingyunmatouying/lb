"""Generate lichess bot leaderboards for each time control and variant.

Process for generating the leaderboards:
 - Call the lichess `get online bots` API (https://lichess.org/api/bot/online).
 - Parse the response into a collection of bots with ratings.
 - Convert collection of bots into leaderboard rows for each time control and variant.
 - Compare that data with data generated previously to create updated leaderboard rows.
 - Save the new data for comparison next time.
 - Generate html leaderboards from the data which are fun to look at.
"""

from src.leaderboard.chrono.fixed_time_provider import FixedTimeProvider
from src.leaderboard.chrono.real_time_provider import RealTimeProvider
from src.leaderboard.fs.real_file_system import RealFileSystem
from src.leaderboard.li.real_lichess_client import RealLichessClient
from src.leaderboard.log.real_log_writer import RealLogWriter
from src.leaderboard.main.leaderboard_generator import LeaderboardGenerator


if __name__ == "__main__":
  # Instantiate dependencies
  file_system = RealFileSystem()
  lichess_client = RealLichessClient()
  time_provider = FixedTimeProvider(RealTimeProvider().get_current_time())
  log_writer = RealLogWriter(__name__)
  # Create generator
  leaderboard_generator = LeaderboardGenerator(file_system, lichess_client, time_provider, log_writer)
  # Generate leaderboards
  leaderboard_generator.generate_leaderboards()
