"""An abstraction for logging."""

import abc


class LogWriter(abc.ABC):
  """Interface for logging."""

  @abc.abstractmethod
  def info(self, message: str, *args: object) -> None:
    """Log at level info."""
    ...
