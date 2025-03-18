"""An implementation of DateProvider which provides the actual current time."""

import time

from src.leaderboard.chrono.time_provider import DateProvider


class RealDateProvider(DateProvider):
  """Provides the current date."""

  def get_current_time(self) -> float:
    """Return the current time."""
    return time.time()
