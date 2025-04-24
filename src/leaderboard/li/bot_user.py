"""Bot user and related dataclasses.

These dataclasses include methods for parsing their corresponding lichess json representations.
"""

import dataclasses
import json
from typing import Any

from src.leaderboard.li.pert_type import PerfType


@dataclasses.dataclass(frozen=True)
class Perf:
  """Performance refers to a players ratings for a particular time control or variant.

  Example game modes include: bullet, blitz, classical, chess960, ...

  In the lichess API the field `perfs` is a list of performances.
  """

  # The time control or variant
  perf_type: PerfType
  # The number of games the bot has played
  games: int
  # The bot's rating for this PerfType
  rating: int
  # The bot's rating deviation
  rd: int
  # The bot's rating change (progress) over the last 12 games
  prog: int
  # If the bot's rating is provisional
  # See: https://lichess.org/faq#provisional
  prov: bool

  @classmethod
  def from_json_dict(cls, perf_type_key: str, perf_json: dict[str, Any]) -> "Perf":
    """Create a Perf based on a json key and value."""
    perf_type = PerfType.from_json(perf_type_key)
    games = perf_json.get("games", 0)
    rating = perf_json.get("rating", 0)
    rd = perf_json.get("rd", 0)
    prog = perf_json.get("prog", 0)
    prov = perf_json.get("prov", False)
    return Perf(perf_type, games, rating, rd, prog, prov)


@dataclasses.dataclass(frozen=True)
class BotUser:
  """A bot user and their list of performances.

  This only contains a small subset of what is available via the lichess API.
  """

  # The bot's username
  username: str
  # The bot's flair
  flair: str
  # The bot's country flag
  flag: str
  # The time the bot was created (seconds since epoch)
  created_at: int
  # If the bot is a patron
  patron: bool
  # If the bot has violated the terms of service
  tos_violation: bool
  # The bot's list of performance ratings
  perfs: list[Perf]

  @classmethod
  def from_json(cls, json_str: str) -> "BotUser":
    """Parse a line of ndjson and converts it to an BotUser."""
    json_dict = json.loads(json_str)

    username = json_dict.get("username", "")
    flair = json_dict.get("flair", "")
    profile_dict = json_dict.get("profile", {})
    flag = profile_dict.get("flag", "")
    created_at = json_dict.get("createdAt", 0) // 1000
    patron = json_dict.get("patron", False)
    tos_violation = json_dict.get("tosViolation", False)

    perfs: list[Perf] = []
    for perf_type_key, perf_json in json_dict.get("perfs", []).items():
      perfs.append(Perf.from_json_dict(perf_type_key, perf_json))

    return BotUser(username, flair, flag, created_at, patron, tos_violation, perfs)
