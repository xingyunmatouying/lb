"""Convert leaderboard data to html."""

import dataclasses

from jinja2 import Environment, FileSystemLoader

from src.leaderboard.chrono import date_formatter
from src.leaderboard.chrono.time_provider import TimeProvider
from src.leaderboard.data.leaderboard_row import LeaderboardRow
from src.leaderboard.li.bot_user import PerfType


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
  last_updated_date: str
  nav_links: list[NavLink]


@dataclasses.dataclass(frozen=True)
class LeaderboardDelta:
  """Convenience class for styling delta columns."""

  formatted_value: str
  html_class: str

  @classmethod
  def for_delta_rank(cls, delta: int, is_new: bool) -> "LeaderboardDelta":
    """Return ↑n, ↓n, "new", or blank."""
    if delta > 0:
      return LeaderboardDelta(f"↑{abs(delta)}", "delta-pos")
    if delta < 0:
      return LeaderboardDelta(f"↓{abs(delta)}", "delta-neg")
    if is_new:
      return LeaderboardDelta("🆕", "")
    return LeaderboardDelta("", "")

  @classmethod
  def for_delta_rating(cls, delta: int) -> "LeaderboardDelta":
    """Return (+n), (-n), or blank."""
    if delta > 0:
      return LeaderboardDelta(f"(+{abs(delta)})", "delta-pos")
    if delta < 0:
      return LeaderboardDelta(f"(-{abs(delta)})", "delta-neg")
    return LeaderboardDelta("", "")


@dataclasses.dataclass(frozen=True)
class HtmlLeaderboardRow:
  """The data required to render a leaderboard row in html."""

  rank: int
  delta_rank: LeaderboardDelta
  username: str
  flag: str
  rating: int
  delta_rating: LeaderboardDelta
  games: int
  created_date: str
  last_seen_date: str

  @classmethod
  def from_leaderboard_row(cls, row: LeaderboardRow) -> "HtmlLeaderboardRow":
    """Convert a LeaderboardRow into an HtmlLeaderboardRow."""
    return HtmlLeaderboardRow(
      row.rank,
      LeaderboardDelta.for_delta_rank(row.delta_rank, row.is_new),
      row.bot_info.profile.username,
      row.bot_info.profile.flag,
      row.bot_info.perf.rating,
      LeaderboardDelta.for_delta_rating(row.delta_rating),
      row.bot_info.perf.games,
      date_formatter.format_yyyy_mm_dd(row.bot_info.profile.created_time),
      date_formatter.format_yyyy_mm_dd(row.bot_info.last_seen_time),
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

  def __init__(self, time_provider: TimeProvider) -> None:
    """Initialize a new generator."""
    self.time_provider = time_provider
    self.jinja_environment = Environment(loader=FileSystemLoader("templates"), autoescape=True, trim_blocks=False)

  def generate_leaderboard_html(self, ranked_rows_by_perf_type: dict[PerfType, list[LeaderboardRow]]) -> dict[str, str]:
    """Generate index and leaderboard html."""
    last_updated_date = date_formatter.format_yyyy_mm_dd_hh_mm_ss(self.time_provider.get_current_time())
    html_by_name: dict[str, str] = {}
    # Create index html
    index_template = self.jinja_environment.get_template("index.html.jinja")
    index_html = index_template.render(
      main_frame=MainFrame("Lichess Bot Leaderboards", last_updated_date, create_nav_links(None))
    )
    html_by_name["index"] = index_html
    # Create leaderboard html
    for perf_type in PerfType.all_except_unknown():
      rows = ranked_rows_by_perf_type.get(perf_type, [])
      leaderboard_template = self.jinja_environment.get_template("leaderboard.html.jinja")
      leaderboard_html = leaderboard_template.render(
        main_frame=MainFrame(perf_type.get_readable_name(), last_updated_date, create_nav_links(perf_type)),
        leaderboard_rows=[HtmlLeaderboardRow.from_leaderboard_row(row) for row in rows],
      )
      html_by_name[perf_type.to_string()] = leaderboard_html
    # Return file name to html contents map
    return html_by_name
