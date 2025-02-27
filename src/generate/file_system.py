"""A representation of a file system."""

import abc


class FileSystem(abc.ABC):
  """Interface for interacting with a file system."""

  @abc.abstractmethod
  def load_file_lines(self, file_name: str) -> list[str]:
    """Load and return all of the lines in a file."""
    ...
