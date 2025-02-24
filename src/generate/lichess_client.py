"""Client for communicating with lichess."""

import abc

from src.generate.online_bot_user import OnlineBotUser


class LichessClient(abc.ABC):
  """Interface for communicating with lichess."""

  @abc.abstractmethod
  def get_online_bots(self) -> list[OnlineBotUser]:
    pass
