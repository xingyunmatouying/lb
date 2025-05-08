"""Tests for flag_emoji.py."""

import unittest

from src.leaderboard.page import flag_emoji


class TestFlagEmoji(unittest.TestCase):
  """Tests for flag_emoji functions."""

  def test_from_string(self) -> None:
    # Regions
    self.assertEqual(flag_emoji.from_string("AQ"), "🇦🇶")  # Antarctica
    self.assertEqual(flag_emoji.from_string("EU"), "🇪🇺")  # European Union
    self.assertEqual(flag_emoji.from_string("FR"), "🇫🇷")  # France
    self.assertEqual(flag_emoji.from_string("DE"), "🇩🇪")  # Germany
    self.assertEqual(flag_emoji.from_string("US"), "🇺🇸")  # United States
    self.assertEqual(flag_emoji.from_string("ZW"), "🇿🇼")  # Zimbabwe
    # Subregions
    self.assertEqual(flag_emoji.from_string("PT-20"), "🏴󠁰󠁴󠀲󠀰󠁿")  # Azores
    self.assertEqual(flag_emoji.from_string("PT-30"), "🏴󠁰󠁴󠀳󠀰󠁿")  # Madeira
    self.assertEqual(flag_emoji.from_string("CA-QC"), "🏴󠁣󠁡󠁱󠁣󠁿")  # Canada - Quebec
    self.assertEqual(flag_emoji.from_string("ES-AN"), "🏴󠁥󠁳󠁡󠁮󠁿")  # Spain - Andalusia
    self.assertEqual(flag_emoji.from_string("ES-AR"), "🏴󠁥󠁳󠁡󠁲󠁿")  # Spain - Aragon
    self.assertEqual(flag_emoji.from_string("ES-AS"), "🏴󠁥󠁳󠁡󠁳󠁿")  # Spain - Asturias
    self.assertEqual(flag_emoji.from_string("ES-CT"), "🏴󠁥󠁳󠁣󠁴󠁿")  # Spain - Catalonia
    self.assertEqual(flag_emoji.from_string("ES-GA"), "🏴󠁥󠁳󠁧󠁡󠁿")  # Spain - Galicia
    self.assertEqual(flag_emoji.from_string("GB-ENG"), "🏴󠁧󠁢󠁥󠁮󠁧󠁿")  # United Kingdom - England
    self.assertEqual(flag_emoji.from_string("GB-NIR"), "🏴󠁧󠁢󠁮󠁩󠁲󠁿")  # United Kingdom - Northern Ireland
    self.assertEqual(flag_emoji.from_string("GB-SCT"), "🏴󠁧󠁢󠁳󠁣󠁴󠁿")  # United Kingdom - Scotland
    self.assertEqual(flag_emoji.from_string("GB-WLS"), "🏴󠁧󠁢󠁷󠁬󠁳󠁿")  # United Kingdom - Wales
    # Overrides
    self.assertEqual(flag_emoji.from_string("_kurdistan"), "🏴󠁩󠁲󠀱󠀶󠁿")  # Kurdistan
    self.assertEqual(flag_emoji.from_string("_adygea"), "🏴󠁲󠁵󠁡󠁤󠁿")  # Russia - Adygea
    self.assertEqual(flag_emoji.from_string("RU-TAT"), "🏴󠁲󠁵󠁴󠁡󠁿")  # Russia - Tatarstan
    self.assertEqual(flag_emoji.from_string("ES-EU"), "🏴󠁥󠁳󠁰󠁶󠁿")  # Spain - Basque Country
    # Other
    self.assertEqual(flag_emoji.from_string("_earth"), "🗺️")  # Earth
    # Unmapped
    self.assertEqual(flag_emoji.from_string("AM-RA"), "")  # Artsakh
    self.assertEqual(flag_emoji.from_string("_belarus-wrw"), "")  # Belarus White-red-white
    self.assertEqual(flag_emoji.from_string("_east-turkestan"), "")  # East Turkestan
    self.assertEqual(flag_emoji.from_string("_russia-wbw"), "")  # Russia White-blue-white

  def test_from_string_lowercase_is_fine(self) -> None:
    self.assertEqual(flag_emoji.from_string("aq"), "🇦🇶")  # Antarctica
    self.assertEqual(flag_emoji.from_string("pt-20"), "🏴󠁰󠁴󠀲󠀰󠁿")  # Azores

  def test_from_string_invalid_is_fine(self) -> None:
    self.assertEqual(flag_emoji.from_string("1"), "")
    self.assertEqual(flag_emoji.from_string("11"), "")
