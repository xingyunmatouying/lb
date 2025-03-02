"""An implementation of DateProvider which provides the actual current date."""

import time

from src.generate import date_provider
from src.generate.date_provider import DateProvider


class RealDateProvider(DateProvider):
  """Provides the current date."""

  def get_current_date(self) -> str:
    """Return the current date formatted as YYYY-MM-DD."""
    return date_provider.format_date(time.time())
