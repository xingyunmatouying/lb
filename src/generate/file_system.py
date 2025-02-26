"""A representation of a file system."""

import abc


class FileSystem(abc.ABC):
  """Interface for interacting with a file system."""

  @abc.abstractmethod
  def load_file_lines(self, file_name: str) -> list[str]:
    """Return all of the lines in a given file."""
    ...
