"""An implementation of LogWriter which actually logs."""

from src.leaderboard.log import logger_creator
from src.leaderboard.log.log_writer import LogWriter


class RealLogWriter(LogWriter):
  """Uses a standard logger which logs to console."""

  def __init__(self, name: str) -> None:
    """Initialize a logger with a specified name."""
    self.logger = logger_creator.create_logger(name)

  def info(self, message: str, *args: object) -> None:
    """Log at level info."""
    self.logger.info(message, *args)
