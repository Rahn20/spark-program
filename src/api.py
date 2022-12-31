#!/usr/bin/python3
# pylint: disable=broad-except

"""
url 1: https://spark.isal.live/api/v1/
url 2: http://localhost:1337/api/v1/
"""

from datetime import datetime
import requests

from src.scooter import Scooter

class ApiData(Scooter):
    """ Api class """

    ## API endpoint URL
    _URL = "http://localhost:1337/api/v1/graphql"

    ## Set the headers
    _HEADERS = {'Content-Type': 'application/json'}


    def __init__(self, user_id: int) -> None:
        """ Initialize class """
        super().__init__()
        self._user_id = user_id
        self._log_id = str


    def get_scooter_data(self, scooter_id: int) -> dict:
        """
        Get scooter data from API.
        """
        ## Create the GraphQL query
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
            ## Send the POST request
            response = requests.post(self._URL, json = payload, headers = self._HEADERS)

            return response.json()["data"]["getScooterById"][0]
        except Exception as error:
            print(error)
            return 0


    def update_scooter(self) -> None:
        """ Update api with scooter's new position, speed, status and battery level. """
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
                'battery': str(int(self.data["battery"])),
                'station_id': str(self.data["station"]),
                'price_id': "1"
            }
        }

        try:
            requests.post(self._URL, json = payload, headers = self._HEADERS)
        except Exception as error:
            print(error)



    def create_log(self) -> None:
        """
        Create log. Data to be added is scooter's position, start date/time and scooter/user id.
        """
        mutation = ''' mutation createLog(
            $scooter_id: String!,
            $customer_id: String!,
            $start_time: String!,
            $start_longitude: String!,
            $start_latitude: String!,
            $price_id: String!) {
                createLog(
                    scooter_id: $scooter_id,
                    customer_id: $customer_id,
                    start_time: $start_time,
                    start_longitude: $start_longitude,
                    start_latitude: $start_latitude,
                    price_id: $price_id) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'scooter_id': self.data["id"],
                'customer_id': str(self._user_id),
                'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'start_longitude': str(self.data["lon"]),
                'start_latitude': str(self.data["lat"]),
                'price_id': "1"
            }
        }

        try:
            response = requests.post(self._URL, json = payload, headers = self._HEADERS)
            data = response.json()["data"]["createLog"][0]

            ## save the log id
            self._log_id = data["id"]
        except Exception as error:
            print(error)


    def update_log(self) -> None:
        """ Update log. Data to be updated is scooter's position and end date/time. """
        mutation = ''' mutation UpdateLogById(
            $id: String!,
            $end_time: String!,
            $end_longitude: String!,
            $end_latitude: String!) {
                UpdateLogById(
                    id: $id,
                    end_time: $end_time,
                    end_longitude: $end_longitude,
                    end_latitude: $end_latitude) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self._log_id,
                'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'end_longitude': str(self.data["lon"]),
                'end_latitude': str(self.data["lat"]),
            }
        }

        try:
            requests.post(self._URL, json = payload, headers = self._HEADERS)
        except Exception as error:
            print(error)


    def get_city_data(self) -> None:
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
            response = requests.post(self._URL, json = payload, headers = self._HEADERS)
            data = response.json()["data"]["getCityByScooterId"][0]

            super().city["id"] = data["id"]
            super().city["area"] = float(data["area"])
            super().city["lat"] = float(data["latitude"])
            super().city["lon"] = float(data["longitude"])

        except Exception as error:
            print(error)


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
            response = requests.post(self._URL, json = payload, headers = self._HEADERS)

            return response.json()["data"]["getStationByCityIdAndZoneId"][0]
        except Exception as error:
            print(error)
            return 0


    def add_scooter(self) -> None:
        """ Add a new scooter."""
        mutation = ''' mutation addScooter(
            $battery: String!,
            $longitude: String!,
            $latitude: String!,
            $price_id: String!,
            $speed: String!,
            $station_id: String!,
            $status_id:String!) {
                addScooter(
                    battery: $battery,
                    longitude: $longitude,
                    latitude: $latitude,
                    speed: $speed,
                    price_id: $price_id,
                    station_id: $station_id,
                    status_id: $status_id) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'status_id': "1",
                'latitude': "59.32511720",
                'longitude': "18.07109350",
                'speed': "0",
                'battery': "70",
                'station_id': "2",
                'price_id': "1"
            }
        }

        try:
            requests.post(self._URL, json = payload, headers = self._HEADERS)
        except Exception as error:
            print(error)


    def create_user(self) -> None:
        """ Create a new user."""
        mutation = ''' mutation createUser(
            $first_name: String!,
            $last_name: String!,
            $password: String!,
            $email: String!,
            $phone: String!,
            $role_id: String!) {
                createUser(
                    first_name: $first_name,
                    last_name: $last_name,
                    password: $password,
                    email: $email,
                    phone: $phone,
                    role_id: $role_id) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'first_name': "Test",
                'last_name': "Testing",
                'password': "1234567891",
                'email': "test@bth.se",
                'phone': "0700000000",
                'role_id': "2",
            }
        }

        try:
            requests.post(self._URL, json = payload, headers = self._HEADERS)
            #print(response.json())
        except Exception as error:
            print(error)
