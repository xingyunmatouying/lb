"""Tests for logger_creator.py."""

import logging
import unittest

from src.leaderboard.log import logger_creator


class TestLoggerCreator(unittest.TestCase):
  """Tests for logger_creator methods."""

  def test_create_logger(self) -> None:
    logger = logger_creator.create_logger(__name__)

    self.assertEqual(logger.name, __name__)
    self.assertEqual(logger.level, logging.INFO)
