"""An implementation of TimeProvider which always provides the time it was instantiated."""

from src.leaderboard.chrono.time_provider import TimeProvider


class FixedTimeProvider(TimeProvider):
  """Provides a fixed time."""

  def __init__(self, fixed_current_time: int) -> None:
    """Set the fixed time based on another TimeProvider."""
    self.fixed_current_time = fixed_current_time

  def get_current_time(self) -> int:
    """Return a fixed time."""
    return self.fixed_current_time
