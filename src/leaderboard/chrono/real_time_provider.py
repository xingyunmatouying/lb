"""An implementation of TimeProvider which provides the actual current time."""

import time

from src.leaderboard.chrono.time_provider import TimeProvider


class RealTimeProvider(TimeProvider):
  """Provides the current time."""

  def get_current_time(self) -> float:
    """Return the current time."""
    return time.time()
