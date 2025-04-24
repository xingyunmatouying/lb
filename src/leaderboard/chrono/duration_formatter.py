"""Functions related to formatting durations."""

import datetime


def get_truncated_datetime(seconds: int) -> datetime.datetime:
  """Convert epoch seconds to a datetime truncated to the day."""
  seconds_datetime = datetime.datetime.fromtimestamp(seconds, tz=datetime.UTC)
  return datetime.datetime(seconds_datetime.year, seconds_datetime.month, seconds_datetime.day, tzinfo=datetime.UTC)


def format_age(start_seconds: int, end_seconds: int) -> str:
  """Calculate age in years and months and return as a readable string."""
  # Be permissive of start and end being switched
  if start_seconds > end_seconds:
    start_seconds, end_seconds = end_seconds, start_seconds

  start_datetime = get_truncated_datetime(start_seconds)
  end_datetime = get_truncated_datetime(end_seconds)

  # Find the age in years and months
  age_months = (end_datetime.year - start_datetime.year) * 12 + (end_datetime.month - start_datetime.month)

  if end_datetime.day < start_datetime.day:
    age_months -= 1

  age_years, age_months = divmod(age_months, 12)

  if age_years == 0:
    return "<1mo" if age_months == 0 else f"{age_months}mo"

  if age_months == 0 and start_datetime.day == end_datetime.day:
    return f"{age_years}y 🎂"

  return f"{age_years}y {age_months}mo"
