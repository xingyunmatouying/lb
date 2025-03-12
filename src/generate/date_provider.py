"""Functions, etc. related to time and dates."""

import abc
import datetime


FORMAT_YYYY_MM_DD = "%Y-%m-%d"


def format_date(epoch_seconds: float, time_format: str) -> str:
  """Convert ms since epoch to YYYY-MM-DD."""
  return datetime.datetime.fromtimestamp(epoch_seconds, tz=datetime.UTC).strftime(time_format)


class DateProvider(abc.ABC):
  """Interface for providing the current date."""

  @abc.abstractmethod
  def get_current_time(self) -> float:
    """Return the current time."""
    ...

  def get_current_date_formatted(self) -> str:
    """Return the current date formatted as YYYY-MM-DD."""
    return format_date(self.get_current_time(), FORMAT_YYYY_MM_DD)
