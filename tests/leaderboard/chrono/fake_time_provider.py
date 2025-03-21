"""Test implementation of TimeProvider which allows setting the current time."""

from src.leaderboard.chrono.time_provider import TimeProvider


class FakeTimeProvider(TimeProvider):
  """A fake implementation of TimeProvider."""

  def __init__(self) -> None:
    """Create a fake time provider and set the current time to 0 (1970-01-01)."""
    self.current_time = 0

  def set_current_time(self, current_time: int) -> None:
    """Set the current time to be returned by get_current_time."""
    self.current_time = current_time

  def get_current_time(self) -> int:
    """Return the current time."""
    return self.current_time
