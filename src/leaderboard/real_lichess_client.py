"""An implementation of LichessClient which actually calls the lichess API."""

import requests

from src.leaderboard.lichess_client import LichessClient


class RealLichessClient(LichessClient):
  """Calls the lichess API."""

  def get_online_bots(self) -> str:
    """Return a list of online bots represented as ndjson.

    Timeout of 10 seconds. No exception handling.
    """
    url = "https://lichess.org/api/bot/online"
    headers = {"Accept": "application/x-ndjson"}
    response = requests.get(url, headers=headers, timeout=10, stream=True)
    response.raise_for_status()
    return response.text
