"""Test implementation of LichessClient which allows setting the response."""

from src.leaderboard.li.lichess_client import LichessClient


class FakeLichessClient(LichessClient):
  """A fake implementation of LichessClient."""

  def __init__(self) -> None:
    """Create a fake lichess client and set the fake response to empty string by default."""
    self.fake_response = ""

  def set_online_bots(self, fake_response: str) -> None:
    """Set the value to be returned by get_online_bots."""
    self.fake_response = fake_response

  def get_online_bots(self) -> str:
    """Return a list of online bots represented as ndjson."""
    return self.fake_response
