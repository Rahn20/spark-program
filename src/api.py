#!/usr/bin/python3
# pylint: disable=broad-except

""" Get and update from the API """

import os
import requests

from src.scooter import Scooter


url = os.environ.get("API_URL")


class ApiData(Scooter):
    """ Api class """
    # API endpoint URL
    _URL = "http://localhost:1337/api/v1/graphql" if url is None else url

    # Set the headers
    _HEADERS = { "Content-Type": "application/json"}


    def __init__(self, user_id: int) -> None:
        """ Initialize class """
        super().__init__()
        self.user_id = user_id
        self.station = ""


    def get_scooter_data(self, scooter_id: int) -> dict:
        """ Get scooter data from API. """
        # Create the GraphQL query
        query = ''' query getScooterById($id: String!) {
            getScooterById(id: $id) {
                id
                latitude
                longitude
                speed
                battery
                status {
                    id
                    status
                }
                station {
                    id
                    station_name
                }
            }
        } '''

        payload = {
            'query': query,
            'variables': {
                'id': str(scooter_id)
            }
        }

        try:
            # Send the POST request
            response = requests.post(self._URL, json=payload, headers=self._HEADERS)

            return response.json()["data"]["getScooterById"][0]
        except (Exception, ConnectionError):
            return -1


    def update_scooter(self) -> None:
        """ Update api with all scooters data. """
        mutation = ''' mutation updateScooterById(
            $id: String!,
            $battery: String!,
            $status_id: String!,
            $longitude: String!,
            $latitude: String!,
            $price_id: String!,
            $speed: String!,
            $station_id: String!) {
                updateScooterById(
                    id: $id,
                    battery: $battery,
                    status_id: $status_id,
                    longitude: $longitude,
                    latitude: $latitude,
                    price_id: $price_id,
                    speed: $speed,
                    station_id: $station_id) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'status_id': str(self.data["status"]),
                'latitude': str(self.data["lat"]),
                'longitude': str(self.data["lon"]),
                'speed': str(self.data["speed"]),
                'battery': str(self.data["battery"]),
                'station_id': str(self.data["station"]),
                'price_id': "1"
            }
        }

        try:
            requests.post(self._URL, json=payload, headers=self._HEADERS)
        except (Exception, ConnectionError) as error:
            print(error)


    def update_rented_scooter(self) -> None:
        """ Update api with scooter's new position, speed, status and battery level. """
        mutation = ''' mutation updateRentedScooterById(
            $id: String!,
            $battery: String!,
            $status_id: String!,
            $longitude: String!,
            $latitude: String!,
            $speed: String!) {
                updateRentedScooterById(
                    id: $id,
                    battery: $battery,
                    status_id: $status_id,
                    longitude: $longitude,
                    latitude: $latitude,
                    speed: $speed)
                    {
                        id
                    }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'status_id': str(self.data["status"]),
                'latitude': str(self.data["lat"]),
                'longitude': str(self.data["lon"]),
                'speed': str(self.data["speed"]),
                'battery': str(self.data["battery"]),
            }
        }

        try:
            requests.post(self._URL, json=payload, headers=self._HEADERS)
        except (Exception, ConnectionError) as error:
            print(error)


    def rent_scooter(self) -> None:
        """
        Create log. Data to be added is scooter's position, start date/time and scooter/user id.
        """
        mutation = ''' mutation rentScooter(
            $id: String!,
            $user_id: String!,
            $longitude: String!,
            $latitude: String!) {
                rentScooter(
                    id: $id,
                    user_id: $user_id,
                    longitude: $longitude,
                    latitude: $latitude)
                    { 
                        id 
                        success
                    }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'user_id': str(self.user_id),
                'longitude': str(self.data["lon"]),
                'latitude': str(self.data["lat"]),
            }
        }

        try:
            response = requests.post(self._URL, json=payload, headers=self._HEADERS)

            # save the station
            self.station = response.json()["data"]["rentScooter"]["success"]
        except (Exception, ConnectionError) as error:
            print(error)


    def return_scooter(self, time: int) -> None:
        """
        Create log. Data to be added is scooter's position, start date/time and scooter/user id.
        """
        mutation = ''' mutation returnScooter(
            $id: String!,
            $user_id: String!,
            $longitude: String!,
            $latitude: String!,
            $time: String!,
            $station: String!) {
                returnScooter(
                    id: $id,
                    user_id: $user_id,
                    longitude: $longitude,
                    latitude: $latitude,
                    time: $time,
                    station: $station)
                    { 
                        success
                    }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'user_id': str(self.user_id),
                'longitude': str(self.data["lon"]),
                'latitude': str(self.data["lat"]),
                'time': str(time),
                'station': self.station
            }
        }

        try:
            requests.post(self._URL, json=payload, headers=self._HEADERS)
        except (Exception, ConnectionError) as error:
            print(error)


    def get_city_data(self) -> dict:
        """
        Get city's center position, id and area where the scooter is located.
        And adds it to city dictionary.
        """
        query = ''' query getCityByScooterId($id: String!) {
            getCityByScooterId(id: $id) {
                id
                latitude
                longitude
                area
            }
        } '''

        payload = {
            'query': query,
            'variables': {
                'id': self.data["id"]
            }
        }

        try:
            response = requests.post(self._URL, json=payload, headers=self._HEADERS)

            return response.json()["data"]["getCityByScooterId"][0]
        except (Exception, ConnectionError):
            return -1


    def get_station(self, zone_id: str) -> dict:
        """
        return random charging/maintenance station data in the city where the scooter is located.
        Zone id: 1- Charging Station, 2- Parking Station, 3- Bike Statione, 4- Maintenance Station.
        """
        query = ''' query getStationByCityIdAndZoneId($cityId: String!, $zoneId: String!) {
            getStationByCityIdAndZoneId(cityId: $cityId, zoneId: $zoneId) {
                id
                latitude
                longitude
            }
        } '''

        payload = {
            'query': query,
            'variables': {
                'cityId': self.city["id"],
                'zoneId': zone_id
            }
        }

        try:
            response = requests.post(self._URL, json=payload, headers=self._HEADERS)

            return response.json()["data"]["getStationByCityIdAndZoneId"][0]
        except (Exception, ConnectionError):
            return -1
