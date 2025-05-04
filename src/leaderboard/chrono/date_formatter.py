"""Functions and constants related to formatting dates."""

import datetime


FORMAT_YYYY_MM_DD_HH_MM_SS = "%Y-%m-%d %H:%M:%S"


def format_time(epoch_seconds: int, time_format: str) -> str:
  """Convert seconds since epoch to a formatted date."""
  return datetime.datetime.fromtimestamp(epoch_seconds, tz=datetime.UTC).strftime(time_format)


def format_yyyy_mm_dd_hh_mm_ss(epoch_seconds: int) -> str:
  """Format seconds since epoch as YYYY-MM-SS HH:MM:SS."""
  return format_time(epoch_seconds, FORMAT_YYYY_MM_DD_HH_MM_SS)
