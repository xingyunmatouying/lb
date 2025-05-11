"""A representation of a file system."""

import abc


class FileSystem(abc.ABC):
  """Interface for interacting with a file system."""

  @abc.abstractmethod
  def read_file(self, file_name: str) -> str | None:
    """Load and return all of the contents of a file."""
    ...

  @abc.abstractmethod
  def write_file(self, file_name: str, file_contents: str) -> None:
    """Save the contents to a file."""
    ...
