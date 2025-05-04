"""Represents the time controls and variants (a.k.a. game modes) available on lichess.

Related lichess documentation:
  - https://lichess.org/faq#time-controls
  - https://lichess.org/variant
"""

from collections.abc import Generator
from enum import Enum


class PerfType(Enum):
  """Represents the time controls and variants (a.k.a. game modes) available on lichess."""

  # Default value
  UNKNOWN = 0

  # Regular time controls...
  # https://en.wikipedia.org/wiki/Fast_chess#Bullet
  BULLET = 1  # <= 179s (< 3m)
  # https://en.wikipedia.org/wiki/Fast_chess#Blitz
  BLITZ = 2  # <= 479s (< 8m)
  # https://en.wikipedia.org/wiki/Fast_chess#Rapid_(FIDE),_quick_(USCF),_or_active
  RAPID = 3  # <= 1499s (< 25m)
  # https://en.wikipedia.org/wiki/Time_control#Classification
  CLASSICAL = 4  # >= 1500s (>= 25m)

  # Asynchronous chess...
  # https://en.wikipedia.org/wiki/Correspondence_chess
  CORRESPONDENCE = 5

  # Variants...
  # https://en.wikipedia.org/wiki/Chess960
  CHESS960 = 6  # https://lichess.org/variant/chess960
  # https://en.wikipedia.org/wiki/Losing_chess
  ANTICHESS = 7  # https://lichess.org/variant/antichess
  # https://en.wikipedia.org/wiki/Three-check_chess
  THREE_CHECK = 8  # https://lichess.org/variant/threeCheck
  # https://en.wikipedia.org/wiki/Atomic_chess
  ATOMIC = 9  # https://lichess.org/variant/atomic
  # https://en.wikipedia.org/wiki/List_of_chess_variants#King_of_the_Hill
  KING_OF_THE_HILL = 10  # https://lichess.org/variant/kingOfTheHill
  # https://en.wikipedia.org/wiki/Crazyhouse
  CRAZYHOUSE = 11  # https://lichess.org/variant/crazyhouse
  # https://en.wikipedia.org/wiki/Dunsany%27s_chess#Horde_chess
  HORDE = 12  # https://lichess.org/variant/horde
  # https://en.wikipedia.org/wiki/V._R._Parton#Racing_Kings
  RACING_KINGS = 13  # https://lichess.org/variant/racingKings

  @classmethod
  def all_except_unknown(cls) -> Generator["PerfType"]:
    """Yield all PerfType values except UNKNOWN."""
    for perf_type in PerfType:
      if perf_type != PerfType.UNKNOWN:
        yield perf_type

  @classmethod
  def from_json(cls, json_str: str) -> "PerfType":
    """Return the corresponding PerfType based on the json representation."""
    name_to_perf_type = {
      "bullet": PerfType.BULLET,
      "blitz": PerfType.BLITZ,
      "rapid": PerfType.RAPID,
      "classical": PerfType.CLASSICAL,
      "correspondence": PerfType.CORRESPONDENCE,
      "chess960": PerfType.CHESS960,
      "antichess": PerfType.ANTICHESS,
      "threeCheck": PerfType.THREE_CHECK,
      "atomic": PerfType.ATOMIC,
      "kingOfTheHill": PerfType.KING_OF_THE_HILL,
      "crazyhouse": PerfType.CRAZYHOUSE,
      "horde": PerfType.HORDE,
      "racingKings": PerfType.RACING_KINGS,
    }
    return name_to_perf_type.get(json_str, PerfType.UNKNOWN)

  def to_string(self) -> str:
    """Return the original string (json) representation."""
    perf_type_to_name = {
      PerfType.BULLET: "bullet",
      PerfType.BLITZ: "blitz",
      PerfType.RAPID: "rapid",
      PerfType.CLASSICAL: "classical",
      PerfType.CORRESPONDENCE: "correspondence",
      PerfType.CHESS960: "chess960",
      PerfType.ANTICHESS: "antichess",
      PerfType.THREE_CHECK: "threeCheck",
      PerfType.ATOMIC: "atomic",
      PerfType.KING_OF_THE_HILL: "kingOfTheHill",
      PerfType.CRAZYHOUSE: "crazyhouse",
      PerfType.HORDE: "horde",
      PerfType.RACING_KINGS: "racingKings",
    }
    return perf_type_to_name.get(self, "unknown")

  def get_readable_name(self) -> str:
    """Return a readable name for the perf type with spaces, ect."""
    perf_type_to_name = {
      PerfType.BULLET: "Bullet",
      PerfType.BLITZ: "Blitz",
      PerfType.RAPID: "Rapid",
      PerfType.CLASSICAL: "Classical",
      PerfType.CORRESPONDENCE: "Correspondence",
      PerfType.CHESS960: "Chess960",
      PerfType.ANTICHESS: "Antichess",
      PerfType.THREE_CHECK: "Three Check",
      PerfType.ATOMIC: "Atomic",
      PerfType.KING_OF_THE_HILL: "King of the Hill",
      PerfType.CRAZYHOUSE: "Crazyhouse",
      PerfType.HORDE: "Horde",
      PerfType.RACING_KINGS: "Racing Kings",
    }
    return perf_type_to_name.get(self, "Unknown")
