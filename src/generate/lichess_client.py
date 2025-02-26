"""Client for communicating with lichess."""

import abc


class LichessClient(abc.ABC):
  """Interface for communicating with lichess."""

  @abc.abstractmethod
  def get_online_bots(self) -> str: ...
