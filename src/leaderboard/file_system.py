"""A representation of a file system."""

import abc


class FileSystem(abc.ABC):
  """Interface for interacting with a file system."""

  @abc.abstractmethod
  def load_file_lines(self, file_name: str) -> list[str]:
    """Load and return all of the lines in a file."""
    ...

  @abc.abstractmethod
  def save_file_lines(self, file_name: str, file_lines: list[str]) -> None:
    """Save all of the lines to a file."""
    ...
