"""Test implementation of FileSystem which saves and loads "files" in memory."""

from src.leaderboard.fs.file_system import FileSystem


class InMemoryFileSystem(FileSystem):
  """Represents a file system as a mapping from str -> list[str]."""

  def __init__(self) -> None:
    """Initialize a dict to represent the file system."""
    self.file_system: dict[str, str] = {}

  def read_file(self, file_name: str) -> str | None:
    """Load and return all of the contents of a file."""
    return self.file_system.get(file_name, "")

  def write_file(self, file_name: str, file_contents: str) -> None:
    """Save the contents to a file."""
    self.file_system[file_name] = file_contents
