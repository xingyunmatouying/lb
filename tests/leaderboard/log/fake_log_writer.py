"""An implementation of LogWriter which does nothing."""

from src.leaderboard.log.log_writer import LogWriter


class FakeLogWriter(LogWriter):
  """Does nothing."""

  def info(self, message: str, *args: object) -> None:
    """Pretend to log at level info."""
