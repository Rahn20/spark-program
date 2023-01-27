#!/usr/bin/env python3
""" Test cases for apiData class. """


import sys
import unittest
from io import StringIO
from unittest.mock import patch
import json

from src.api import ApiData


# dummy data
with open('tests/dummy.json', 'r', encoding='utf-8') as file:
    DATA = json.load(file)


class TestApi(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """

    def setUp(self) -> None:
        """ Create object for all tests """
        self.api = ApiData(user_id = 1)

        # Fake data
        self.api.data = {
            "id": "1",
            "lat": 59.193475,
            "lon":  17.640142,
            "speed": 0,
            "battery": 80.0,
            "status": "1",
            "station": "2"
        }

    def tearDown(self) -> None:
        """ Remove dependencies after test. """
        self.api = None


    @patch('requests.post')
    def test_get_scooter_data_success(self, mock_post):
        """ Test to return scooters API data when request succeeds. """
        mock_post.return_value.json.return_value = {
            'data': {
                'getScooterById': DATA[0]["getScooterById"]
            }
        }

        scooter_data = self.api.get_scooter_data(1)

        # Assert that the returned data is correct
        self.assertEqual(scooter_data, DATA[0]["getScooterById"][0])


    @patch('requests.post')
    def test_get_scooter_data_error(self, mock_post):
        """ Test to return -1 when request fails."""
        mock_post.side_effect = Exception('Request failed')
        act = self.api.get_scooter_data(1)

        self.assertEqual(act, -1)


    @patch('requests.post')
    def test_update_scooter_success(self, mock_post):
        """ Test to return None and get nothing printed when request succeeds."""
        mock_post.return_value.json.return_value = {
            'data': { None }
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        act = self.api.update_scooter()

        sys.stdout = sys.__stdout__

        self.assertIsNone(act)
        self.assertEqual(captured_output.getvalue(), '')


    @patch('requests.post')
    def test_update_scooter_error(self, mock_post):
        """ Test to print error message when request fails. """
        mock_post.side_effect = Exception('Request failed update scooter')

        captured_output = StringIO()
        sys.stdout = captured_output
        self.api.update_scooter()
        sys.stdout = sys.__stdout__

        # Check that the output is correct
        self.assertEqual(captured_output.getvalue(), 'Request failed update scooter\n')


    @patch('requests.post')
    def test_update_rented_scooter_success(self, mock_post):
        """ Test to return None and get nothing printed when request succeeds."""
        mock_post.return_value.json.return_value = {
            'data': { None }
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        act = self.api.update_rented_scooter()

        sys.stdout = sys.__stdout__

        self.assertIsNone(act)
        self.assertEqual(captured_output.getvalue(), '')


    @patch('requests.post')
    def test_update_rented_scooter_error(self, mock_post):
        """ Test to print error message when request fails. """
        mock_post.side_effect = Exception('Request failed update rented scooter')

        captured_output = StringIO()
        sys.stdout = captured_output
        self.api.update_rented_scooter()
        sys.stdout = sys.__stdout__

        # Check that the output is correct
        self.assertEqual(captured_output.getvalue(), 'Request failed update rented scooter\n')


    @patch('requests.post')
    def test_rent_scooter_success(self, mock_post):
        """ Test to return None and get log id updated when request succeeds."""
        self.api.user_id = "3"

        mock_post.return_value.json.return_value = {
            'data': {
                'rentScooter': { "success": "Station" }
            }
        }
        act = self.api.rent_scooter()

        self.assertIsNone(act)
        self.assertEqual(self.api.station, "Station")


    @patch('requests.post')
    def test_rent_scooter_error(self, mock_post):
        """ Test to print error message when request fails. """
        self.api.user_id = "3"
        mock_post.side_effect = Exception('Request failed')

        captured_output = StringIO()
        sys.stdout = captured_output
        self.api.rent_scooter()
        sys.stdout = sys.__stdout__

        # Check that the output is correct
        self.assertEqual(captured_output.getvalue(), 'Request failed\n')
        self.assertEqual(self.api.station, "")



    @patch('requests.post')
    def test_return_scooter_success(self, mock_post):
        """ Test to return None and get nothing printed when request succeeds. """
        self.api.station = "Station"

        mock_post.return_value.json.return_value = {
            'data': { None }
        }

        captured_output = StringIO()
        sys.stdout = captured_output

        act = self.api.return_scooter(time = 3)

        sys.stdout = sys.__stdout__
        self.assertIsNone(act)
        self.assertEqual(captured_output.getvalue(), '')


    @patch('requests.post')
    def test_return_scooter_error(self, mock_post):
        """ Test to print error message when request fails. """
        self.api.station = "Station"
        mock_post.side_effect = Exception('Request failed update log')

        captured_output = StringIO()
        sys.stdout = captured_output
        self.api.return_scooter(time = 2)
        sys.stdout = sys.__stdout__

        # Check that the output is correct
        self.assertEqual(captured_output.getvalue(), 'Request failed update log\n')



    @patch('requests.post')
    def test_get_city_data_success(self, mock_post):
        """ Test to return citys API data when request succeeds. """
        mock_post.return_value.json.return_value = {
            'data': {
                'getCityByScooterId': DATA[0]["getCityByScooterId"]
            }
        }

        city_data = self.api.get_city_data()
    
        # Assert that the returned data is correct
        self.assertEqual(city_data, DATA[0]["getCityByScooterId"][0])


    @patch('requests.post')
    def test_get_city_data_error(self, mock_post):
        """ Test to print error message when request fails. """
        mock_post.side_effect = ConnectionError('Connection failed')
        act = self.api.get_city_data()

        self.assertEqual(act, -1)


    @patch('requests.post')
    def test_get_station_success(self, mock_post):
        """ Test to return stations API data when request succeeds."""
        self.api.city["id"] = "1"

        mock_post.return_value.json.return_value = {
            'data': {
                'getStationByCityIdAndZoneId': DATA[0]["getStationByCityIdAndZoneId"]
            }
        }

        station_data = self.api.get_station(zone_id = "2")

        self.assertEqual(station_data, DATA[0]["getStationByCityIdAndZoneId"][0])


    @patch('requests.post')
    def test_get_station_error(self, mock_post):
        """ Test to return -1 when request fails. """
        self.api.city["id"] = "1"

        mock_post.side_effect = ConnectionError('Connection failed')
        act = self.api.get_station(zone_id = "2")

        self.assertEqual(act, -1)
