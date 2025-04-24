"""Module providing a function for converting a dataclass to a dict."""

import typing
from typing import Any


def to_dict_without_defaults(data_class_dict: dict[str, Any]) -> dict[str, Any]:
  """Convert a dataclass into a dict, but leave out unset/default values."""
  dict_with_no_defaults: dict[str, Any] = {}
  for name, value in data_class_dict.items():
    dict_value = value
    if isinstance(value, dict):
      # We should be able to assume this is always dict[str, Any]
      cast_dict = typing.cast(dict[str, Any], value)  # We need to cast for the type checker
      dict_value = to_dict_without_defaults(cast_dict)
    if dict_value:
      dict_with_no_defaults[name] = dict_value
  return dict_with_no_defaults
