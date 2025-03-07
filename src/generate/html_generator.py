"""Convert leaderboard data to html."""

import dataclasses

from jinja2 import Environment, FileSystemLoader

from src.generate.file_system import FileSystem
from src.generate.leaderboard_data import LeaderboardRow
from src.generate.lichess_bot_user import PerfType


@dataclasses.dataclass(frozen=True)
class NavLink:
  """An element of the navigation bar."""

  link: str
  name: str
  is_active: bool


@dataclasses.dataclass(frozen=True)
class MainFrame:
  """The main frame which is shared by the index and all of the leaderboard pages."""

  title: str
  nav_links: list[NavLink]


@dataclasses.dataclass(frozen=True)
class HtmlLeaderboardRow:
  """The data required to render a leaderboard row in html."""

  rank: int
  rank_delta: int
  username: str
  flag: str
  rating: int
  rating_delta: int
  games: int
  created_date: str
  last_seen_date: str
  is_new: bool

  @classmethod
  def from_leaderboard_row(cls, row: LeaderboardRow) -> "HtmlLeaderboardRow":
    """Convert a LeaderboardRow into an HtmlLeaderboardRow."""
    return HtmlLeaderboardRow(
      row.rank,
      row.rank_delta,
      row.perf.username,
      row.perf.flag,
      row.perf.rating,
      row.rating_delta,
      row.perf.games,
      row.perf.created_date,
      row.perf.last_seen_date,
      row.is_new,
    )


def create_nav_links(active_perf_type: PerfType | None) -> list[NavLink]:
  """Create the list of nav links shared by all pages.

  This also sets the active perf type to highlight the current page.
  """
  nav_links: list[NavLink] = []
  nav_links.append(NavLink("index.html", "Home", active_perf_type is None))
  nav_links.extend(
    NavLink(f"{perf_type.to_string()}.html", perf_type.get_readable_name(), perf_type == active_perf_type)
    for perf_type in PerfType.all_except_unknown()
  )
  return nav_links


class LeaderboardHtmlGenerator:
  """Generator for html."""

  def __init__(self, file_system: FileSystem) -> None:
    """Initialize a new generator."""
    self.file_system: FileSystem = file_system
    self.jinja_environment = Environment(loader=FileSystemLoader("templates"), autoescape=True, trim_blocks=False)

  def generate_leaderboard_html(self, ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]]) -> None:
    """Generate and save all leaderboard html."""
    html_by_name: dict[str, str] = {}
    # Create index
    index_template = self.jinja_environment.get_template("index.html.jinja")
    index_html = index_template.render(main_frame=MainFrame("Lichess Bot Leaderboards", create_nav_links(None)))
    html_by_name["leaderboard_html/index.html"] = index_html
    # Create leaderboards
    for perf_type in PerfType.all_except_unknown():
      rows = ranked_rows_by_perf_type.get(perf_type, [])
      leaderboard_template = self.jinja_environment.get_template("leaderboard.html.jinja")
      leaderboard_html = leaderboard_template.render(
        main_frame=MainFrame(perf_type.get_readable_name(), create_nav_links(perf_type)),
        leaderboard_rows=[HtmlLeaderboardRow.from_leaderboard_row(row) for row in rows],
      )
      html_by_name[f"leaderboard_html/{perf_type.to_string()}.html"] = leaderboard_html
    # Save files
    for file_name, contents in html_by_name.items():
      self.file_system.save_file_lines(file_name, [contents])
