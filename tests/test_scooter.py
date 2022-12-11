#!/usr/bin/env python3
""" Test cases for Scooter class. """


import unittest
from src.scooter import Scooter


class TestScooter(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """

    def setUp(self) -> None:
        """ Create object for all tests """
        self.scooter = Scooter()


    def tearDown(self) -> None:
        """ Remove dependencies after test. """
        self.scooter = None
