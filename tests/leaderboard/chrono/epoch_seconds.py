"""Constants and functions related to epoch-second representations of dates."""

import datetime


DATE_2021_04_01 = 1617300000

DATE_2022_04_01 = 1648800000

DATE_2023_04_01 = 1680350000

DATE_2024_01_01 = 1704100000
DATE_2024_04_01 = 1712000000

DATE_2025_04_01 = 1743500000


def from_date(year: int, month: int, day: int, hour: int = 0, minute: int = 0) -> int:
  """Return the number of seconds since epoch for a given date."""
  return int(datetime.datetime(year, month, day, hour, minute, tzinfo=datetime.UTC).timestamp())
