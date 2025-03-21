"""An abstraction for providing the current time."""

import abc


class TimeProvider(abc.ABC):
  """Interface for providing the current time."""

  @abc.abstractmethod
  def get_current_time(self) -> int:
    """Return the current time."""
    ...
