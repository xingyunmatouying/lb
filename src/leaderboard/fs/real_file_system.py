"""An implementation of FileSystem which actually writes to and from disk."""

from pathlib import Path

from src.leaderboard.fs.file_system import FileSystem


class RealFileSystem(FileSystem):
  """Read and write files from disk."""

  def read_file(self, file_name: str) -> str | None:
    """Load and return all of the contents of a file."""
    path = Path(file_name)
    if not path.exists():
      return None
    with path.open() as file:
      return file.read()

  def write_file(self, file_name: str, file_contents: str) -> None:
    """Save the contents to a file."""
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
      file.write(file_contents)
