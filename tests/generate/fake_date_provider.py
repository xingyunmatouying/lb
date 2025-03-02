"""Test implementation of DateProvider which allows setting the current date."""

from src.generate.date_provider import DateProvider


class FakeDateProvider(DateProvider):
  """A fake implementation of DateProvider."""

  def __init__(self) -> None:
    """Create a fake date provider and set the current date to 1970-01-01."""
    self.current_date = "1970-01-01"

  def set_current_date(self, current_date: str) -> None:
    """Set the current date to be returned by get_current_date."""
    self.current_date = current_date

  def get_current_date(self) -> str:
    """Return the current date."""
    return self.current_date
