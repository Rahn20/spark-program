#!/usr/bin/env python3
""" Test cases for Scooter class. """


import unittest
from unittest.mock import patch

from src.scooter import Scooter


class TestScooter(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """

    def setUp(self) -> None:
        """ Create object for all tests """
        self.scooter = Scooter()

        # creates fake city and scooter data
        self.scooter.data = {
            "id": "1",
            "lat": 59.193475,
            "lon":  17.640142,
            "speed": 0,
            "battery": 100.0,
            "status": "1",
            "station": "2"
        }

        self.scooter.city = {
            "id": "2",
            "area": 25.84,
            "lat": 59.19554,
            "lon": 17.62525
        }


    def tearDown(self) -> None:
        """ Remove dependencies after test. """
        self.scooter = None


    def test_check_scooter_status_true(self):
        """
        Test to return True when status id is 1 (Available)
        and add data to scooter dictionary.
        """
        # Act
        act = self.scooter.check_scooter_status({
            "status": {"id": "1"},
            "id": "12",
            "latitude": str(59.0000),
            "longitude":  str(17.00000),
            "speed": str(0),
            "battery": str(90),
        })

        # Assert
        self.assertTrue(act)
        self.assertEqual(self.scooter.data, {
            "id": "12",
            "lat": 59.0000,
            "lon":  17.00000,
            "speed": 0,
            "battery": 90.0,
            "status": "7",
            "station": None
        })


    def test_check_scooter_status_false(self):
        """ Test to return False when status id is not 1 (Available) """
        # Act
        act = self.scooter.check_scooter_status({
            "status": {"id": "2"},
        })

        # Assert
        self.assertFalse(act)


    def test_return_str(self):
        """ Test to return string with scooter data. """
        # Arrange
        expect = "Scooter id: 1\nLocation: 59.193475, 17.640142\nSpeed: 0km/h\nBattery: 100.0%"

        # Act
        actual = self.scooter.__str__()

        # Assert
        self.assertEqual(actual, expect)


    def test_move_scooter(self):
        """ Test to move the scooter to a random location. """
        # Arrange
        self.scooter.location = "Point(56.00000, 18.0000, 0.0)"

        # Act
        self.scooter.move_scooter()

        # Assert
        self.assertEqual(self.scooter.data["lat"], 56.00000)
        self.assertEqual(self.scooter.data["lon"], 18.0000)
        self.assertEqual(self.scooter.data["battery"], 99.5)


    def test_change_location(self):
        """ Test to change scooter location. """
        # Act
        self.scooter.change_location()

        # Assert
        self.assertNotEqual(self.scooter.location, "")


    def test_stop_scooter(self):
        """ Test to stop the scooter from running. """
        # Act
        self.scooter.stop_scooter("2")

        # Assert
        self.assertEqual(self.scooter.data["status"], "2")
        self.assertEqual(self.scooter.data["speed"], 0)


    def test_check_battery_true(self):
        """ Test to return True when battery level is < 20% """
        # Arrange
        self.scooter.data["battery"] = 19

        # Act
        act = self.scooter.check_battery()

        # Assert
        self.assertTrue(act)


    def test_check_battery_false(self):
        """ Test to return False when battery level is >= 20%. """
        # Arrange
        self.scooter.data["battery"] = 50

        # Act
        act = self.scooter.check_battery()

        # Assert
        self.assertFalse(act)


    def test_move_to_station(self):
        """ Test to move scooter to a specific station location. """
        # Act
        self.scooter.move_to_station({"latitude": 44.22, "longitude":  12.99, "id": "5"})

        # Assert
        self.assertEqual(self.scooter.data["lat"], 44.22)
        self.assertEqual(self.scooter.data["lon"], 12.99)
        self.assertEqual(self.scooter.data["station"], "5")


    @patch('random.randint')
    def test_check_maintenance_false(self, mock_randint):
        """ Test to return False when random.randint is not equal to 1. """
        # Arrange, set the return value of the mock randint function
        mock_randint.return_value = 5

        # Act, call the function and check the result
        act = self.scooter.check_maintenance()

        # Assert
        self.assertFalse(act)


    @patch('random.randint')
    def test_check_maintenance_true(self, mock_randint):
        """ Test to return True when random.randint is equal to 1. """
        # Arrange, set the return value of the mock randint function
        mock_randint.return_value = 1

        # Act, call the function and check the result
        act = self.scooter.check_maintenance()

        # Assert
        self.assertTrue(act)


    def test_check_scooter_in_city_true(self):
        """ Test to return True if scooter is inside of the city zone. """
        # Act
        act = self.scooter.check_scooter_in_city()

        # Assert
        self.assertTrue(act)


    def test_check_scooter_in_city_false(self):
        """ Test to return False if scooter is outside of the city zone."""
        # Arrange
        self.scooter.data["lon"] = 17.606871
        self.scooter.data["lat"] = 59.159111

        # Act
        act = self.scooter.check_scooter_in_city()

        # Assert
        self.assertFalse(act)
