"""An implementation of FileSystem which actually writes to and from disk."""

from pathlib import Path

from src.leaderboard.file_system import FileSystem


class RealFileSystem(FileSystem):
  """Read and write files from disk."""

  def load_file_lines(self, file_name: str) -> list[str]:
    """Load and return all of the lines in a file."""
    path = Path(file_name)
    if not path.exists():
      return []
    with path.open() as file:
      return [line.strip("\n") for line in file.readlines()]

  def save_file_lines(self, file_name: str, file_lines: list[str]) -> None:
    """Save all of the lines to a file."""
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
      file.writelines([f"{line}\n" for line in file_lines])
