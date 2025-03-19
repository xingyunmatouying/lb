"""Test implementation of FileSystem which saves and loads "files" in memory."""

from src.leaderboard.fs.file_system import FileSystem


class InMemoryFileSystem(FileSystem):
  """Represents a file system as a mapping from str -> list[str]."""

  def __init__(self) -> None:
    """Initialize a dict to represent the file system."""
    self.file_system: dict[str, list[str]] = {}

  def load_file_lines(self, file_name: str) -> list[str]:
    """Load and return all of the lines in a file."""
    return self.file_system.get(file_name, [])

  def save_file_lines(self, file_name: str, file_lines: list[str]) -> None:
    """Save all of the lines to a file."""
    self.file_system[file_name] = file_lines
