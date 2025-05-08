"""Module containing logic related to flag emojis.

The options on Lichess are: https://github.com/lichess-org/lila/blob/master/modules/user/src/main/Flags.scala.
"""

# Two-character ISO 3166-1 country codes
STANDARD_REGION_CODE_LENGTH = 2

# The difference between ascii "A" and the region indicator "🇦"
FLAG_LETTER_MAGIC = ord("🇦") - ord("A")
# The difference between ascii "A" and the tag Latin small letter A.
SUBREGION_FLAG_LETTER_MAGIC = ord("\U000e0061") - ord("A")
# The difference between ascii "0" and the tag Latin small letter 0.
SUBREGION_FLAG_NUMBER_MAGIC = ord("\U000e0030") - ord("0")

# The black flag begins the subregion tag sequence - https://emojipedia.org/emoji-tag-sequence
BLACK_FLAG_EMOJI = "🏴"
# The cancel tag ends the sequence - https://en.wikipedia.org/wiki/Tags_(Unicode_block)#Current_use
CANCEL_TAG = "\U000e007f"

# In some cases lichess does not follow the regular standard
OVERRIDES = {
  "_kurdistan": "IR-16",  # Kurdistan
  "_adygea": "RU-AD",  # Russia - Adygea
  "RU-TAT": "RU-TA",  # Russia - Tatarstan
  "ES-EU": "ES-PV",  # Spain - Basque Country
  "_united-nations": "UN",  # United Nations
}

# In some cases lichess uses flags which do not map to standard flag emojis
UNMAPPED = [
  "AM-RA",  # Artsakh
  "_belarus-wrw",  # Belarus White-red-white
  "_east-turkestan",  # East Turkestan
  "_russia-wbw",  # Russia White-blue-white
]

# How lichess represents the earth flag option
LICHESS_EARTH_FLAG_STR = "_earth"
# There is not an exact equivalent for the earth flag lichess uses
EARTH_FLAG_EMOJI = "🗺️"


def region_indicator(char: str) -> str:
  """Convert a letter to the corresponding region indicator symbol."""
  return chr(ord(char.upper()) + FLAG_LETTER_MAGIC) if char.isalpha() else ""


def tag_small_latin(char: str) -> str:
  """Convert a letter or number to the corresponding tag latin small character."""
  if char.isdigit():
    return chr(ord(char) + SUBREGION_FLAG_NUMBER_MAGIC)
  if char.isalpha():
    return chr(ord(char.upper()) + SUBREGION_FLAG_LETTER_MAGIC)
  return ""


def from_string(flag_str: str) -> str:
  """Create a flag emoji based on the flag string used by lichess."""
  if flag_str in UNMAPPED:
    # Don't attempt to find a flag in cases where we know there isn't one
    return ""
  if flag_str in OVERRIDES:
    return from_string(OVERRIDES[flag_str])
  if len(flag_str) == STANDARD_REGION_CODE_LENGTH:
    return "".join(region_indicator(char) for char in flag_str)
  if "-" in flag_str:
    subregion_str = "".join(tag_small_latin(char) for char in flag_str)
    return f"{BLACK_FLAG_EMOJI}{subregion_str}{CANCEL_TAG}"
  if flag_str == LICHESS_EARTH_FLAG_STR:
    return EARTH_FLAG_EMOJI
  # We tried
  return ""
