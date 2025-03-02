"""Functions, etc. related to time and dates."""

import abc
import datetime


def format_date(epoch_seconds: float) -> str:
  """Convert ms since epoch to YYYY-MM-DD."""
  return datetime.datetime.fromtimestamp(epoch_seconds, tz=datetime.UTC).strftime("%Y-%m-%d")


class DateProvider(abc.ABC):
  """Interface for providing the current date."""

  @abc.abstractmethod
  def get_current_date(self) -> str:
    """Return the current date formatted as YYYY-MM-DD."""
    ...
