import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class Perf:
  """
  Performance refers to a players ratings for a particular time control or variant.

  Example game modes include: bullet, blitz, classical, chess960, ...

  In the lichess API the field `perfs` is a list of performances. Not all fields are represented here.
  """

  perf_type: str

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


def from_json(json_str: str) -> OnlineBotUser:
  """Parse a line of ndjson and converts it to an OnlineBotUser."""
  json_dict = json.loads(json_str)
  username = json_dict.get("username", "")
  perfs_dict = json_dict.get("perfs", [])
  perfs: list[Perf] = []
  for perf_type, perf_json in perfs_dict.items():
    games = perf_json.get("games", 0)
    rating = perf_json.get("rating", 0)
    prov = perf_json.get("prov", False)
    perfs.append(Perf(perf_type, games, rating, prov))

  return OnlineBotUser(username, perfs)
