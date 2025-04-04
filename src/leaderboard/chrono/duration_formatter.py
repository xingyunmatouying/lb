"""Functions related to formatting durations."""

import datetime


def format_age(start_seconds: int, end_seconds: int) -> str:
  """Calculate age in years and months and return as a readable string."""
  # Be permissive of start and end being switched
  if start_seconds > end_seconds:
    start_seconds, end_seconds = end_seconds, start_seconds

  start_datetime = datetime.datetime.fromtimestamp(start_seconds, tz=datetime.UTC)
  end_datetime = datetime.datetime.fromtimestamp(end_seconds, tz=datetime.UTC)

  # Truncate to the day for simplicity
  start_datetime = datetime.datetime(start_datetime.year, start_datetime.month, start_datetime.day, tzinfo=datetime.UTC)
  end_datetime = datetime.datetime(end_datetime.year, end_datetime.month, end_datetime.day, tzinfo=datetime.UTC)

  # Find the age in years and months
  age_years = end_datetime.year - start_datetime.year
  age_months = end_datetime.month - start_datetime.month

  if age_months < 0:
    age_years -= 1
    age_months += 12

  if end_datetime.day < start_datetime.day:
    if age_months == 0:
      age_years -= 1
      age_months += 11
    else:
      age_months -= 1

  if age_years == 0 and age_months == 0:
    return "<1mo"

  age_years_str = f"{age_years}y " if age_years else ""
  return f"{age_years_str}{age_months}mo"
