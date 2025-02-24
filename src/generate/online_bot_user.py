"""
Bot user and related dataclasses.

These dataclasses include functions for parsing their corresponding lichess json representations.
"""

import dataclasses
import json
from enum import Enum


class PerfType(Enum):
  """
  Represents the time controls and variants (a.k.a. game modes) available on lichess.

  Related lichess documentation:
    - https://lichess.org/faq#time-controls
    - https://lichess.org/variant
  """

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
  # https://en.wikipedia.org/wiki/Crazyhouse
  CRAZYHOUSE = 6  # https://lichess.org/variant/crazyhouse
  # https://en.wikipedia.org/wiki/Chess960
  CHESS960 = 7  # https://lichess.org/variant/chess960
  # https://en.wikipedia.org/wiki/List_of_chess_variants#King_of_the_Hill
  KING_OF_THE_HILL = 8  # https://lichess.org/variant/kingOfTheHill
  # https://en.wikipedia.org/wiki/Losing_chess
  ANTICHESS = 9  # https://lichess.org/variant/antichess
  # https://en.wikipedia.org/wiki/Three-check_chess
  THREE_CHECK = 10  # https://lichess.org/variant/threeCheck
  # https://en.wikipedia.org/wiki/Atomic_chess
  ATOMIC = 11  # https://lichess.org/variant/atomic
  # https://en.wikipedia.org/wiki/Dunsany%27s_chess#Horde_chess
  HORDE = 12  # https://lichess.org/variant/horde
  # https://en.wikipedia.org/wiki/V._R._Parton#Racing_Kings
  RACING_KINGS = 13  # https://lichess.org/variant/racingKings

  @classmethod
  def from_json(cls, json_str: str) -> "PerfType":
    match json_str:
      case "bullet":
        return PerfType.BULLET
      case "blitz":
        return PerfType.BLITZ
      case "rapid":
        return PerfType.RAPID
      case "classical":
        return PerfType.CLASSICAL
      case "correspondence":
        return PerfType.CORRESPONDENCE
      case "crazyhouse":
        return PerfType.CRAZYHOUSE
      case "chess960":
        return PerfType.CHESS960
      case "kingOfTheHill":
        return PerfType.KING_OF_THE_HILL
      case "antichess":
        return PerfType.ANTICHESS
      case "threeCheck":
        return PerfType.THREE_CHECK
      case "atomic":
        return PerfType.ATOMIC
      case "horde":
        return PerfType.HORDE
      case "racingKings":
        return PerfType.RACING_KINGS
      case _:
        return PerfType.UNKNOWN


@dataclasses.dataclass(frozen=True)
class Perf:
  """
  Performance refers to a players ratings for a particular time control or variant.

  Example game modes include: bullet, blitz, classical, chess960, ...

  In the lichess API the field `perfs` is a list of performances. Not all fields are represented here.
  """

  perf_type: PerfType

  games: int

  rating: int

  prov: bool


@dataclasses.dataclass(frozen=True)
class OnlineBotUser:
  """
  A bot user and their list of performances.

  This only contains a small subset of what is available via the lichess API.
  """

  username: str

  perfs: list[Perf]

  @classmethod
  def from_json(cls, json_str: str) -> "OnlineBotUser":
    """Parse a line of ndjson and converts it to an OnlineBotUser."""
    json_dict = json.loads(json_str)
    username = json_dict.get("username", "")
    perfs_dict = json_dict.get("perfs", [])

    perfs: list[Perf] = []
    for perf_type_str, perf_json in perfs_dict.items():
      games = perf_json.get("games", 0)
      rating = perf_json.get("rating", 0)
      prov = perf_json.get("prov", False)
      perf_type = PerfType.from_json(perf_type_str)
      perfs.append(Perf(perf_type, games, rating, prov))

    return OnlineBotUser(username, perfs)
