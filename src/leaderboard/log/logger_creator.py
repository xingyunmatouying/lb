"""Module containing a function for creating a logger."""

import logging


def create_logger(name: str) -> logging.Logger:
  """Initialize and return a logger."""
  logger = logging.getLogger(name)
  logger.setLevel(logging.INFO)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)
  stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
  logger.addHandler(stream_handler)
  return logger
