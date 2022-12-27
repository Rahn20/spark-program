#!/usr/bin/python3

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
    _URL = "http://localhost:1337/api/v1/"

    ## Set the headers
    _HEADERS = {'Content-Type': 'application/json'}


    def __init__(self, user_id: int) -> None:
        """ Initialize class """
        super().__init__()
        self._user_id = user_id
        self._log_id = int


    def check_scooter_status(self, scooter_id: int) -> bool:
        """
        Check scooter status. Returns true if the scooter is available
        and adds the scooter's data to data dictionary.
        """
        ## Create the GraphQL query
        #query = ''' query getScooterById($id: Int) {
        #    getScooterById(id: $id) {
        #        latitude
        #        longitude
        #        speed
        #        battery
        #        status
        #    }
        #} '''

        #payload = {
        #    'query': query,
        #    'variables': {
        #        'id': scooter_id
        #    }
        #}

        ## Send the POST request
        #response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        #print(response.json())
        # print(query)

        # if status == "available":
        # self.add_scooter_data(response.json())
        #  return True
        # otherwise False

        # returns true to test
        self.data["id"] = scooter_id
        return True


    def connect_user(self) -> None:
        """ Connect user to scooter. """
        mutation = ''' mutation updateScooter($id: Int!, $user_id: Int!) {
            updateScooter(id: $id, user_id: $user_id) {
                data
            }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'user_id': self._user_id
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        print(response.json())


    def remove_user_connection(self) -> None:
        """ Remove connection between user and scooter. """
        mutation = ''' mutation updateScooter($id: Int!, $user_id: Int!) {
            updateScooter(id: $id, user_id: $user_id) {
                data
            }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'user_id': None
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        print(response.json())


    def update_scooter(self) -> None:
        """ Update api with scooter's new position, speed, status and battery level. """
        mutation = ''' mutation updateScooter(
            $id: Int!,
            $user_id: Int!,
            $latitude: Float!,
            $longitude: Float!,
            $speed: Int!,
            $battery: Float!,
            $status: String!) {
                updateScooter(
                    id: $id,
                    user_id: $user_id,
                    latitude: $latitude,
                    longitude: $longitude,
                    speed: $speed,
                    battery: $battery
                    status: $status) { data }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self.data["id"],
                'user_id': self._user_id,
                'latitude': self.data["lat"],
                'longitude': self.data["lon"],
                'speed': self.data["speed"],
                'battery': self.data["battery"],
                'status': self.data["status"]
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        print(response.json())


    def create_log(self) -> None:
        """
        Create log. Data to be added is scooter's position, start date/time and scooter/user id.
        """
        mutation = ''' mutation createLog(
            $scooter_id: Int!,
            $user_id: Int!,
            $start_time: Datetime,
            $start_longitude: Float!,
            $start_latitude: Float!) {
                createLog(
                    scooter_id: $scooter_id,
                    user_id: $user_id,
                    start_time: $start_time,
                    start_longitude: $start_longitude,
                    start_latitude: $start_latitude) { id }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'scooter_id': self.data["id"],
                'user_id': self._user_id,
                'start_time': datetime.now(),
                'start_longitude': self.data["lon"],
                'start_latitude': self.data["lat"],
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        # save the log id
        # self._log_id =
        print(response.json())


    def update_log(self) -> None:
        """ Update log. Data to be updated is scooter's position and end date/time. """
        mutation = ''' mutation updateLog(
            $id: Int!,
            $end_time: Datetime,
            $end_longitude: Float!,
            $end_latitude: Float!) {
                updateLog(
                    id: $id,
                    end_time: $end_time,
                    end_longitude: $end_longitude
                    end_latitude: $end_latitude)
                    { data }
        } '''

        payload = {
            'query': mutation,
            'variables': {
                'id': self._log_id,
                'end_time': datetime.now(),
                'end_longitude': self.data["lon"],
                'end_latitude': self.data["lat"]
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        print(response.json())


    def get_city_data(self) -> None:
        """
        Get city's center position, id and area where the scooter is running.
        And adds it to city dictionary.
        """
        query = ''' query getCityData($scooter_id: Int) {
            getCityData(scooter_id: $scooter_id) {
                id
                latitude
                longitude
                area
            }
        } '''

        payload = {
            'query': query,
            'variables': {
                'scooter_id': self.data["id"]
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        #
        #self.city = {
        #    "id": ,
        #    "area":,      # km²
        #    "lat": ,    # coordinates
        #    "lon":      # coordinates
        #}
        print(response.json())


    def get_station(self, station_type: str) -> dict:
        """
        return random charging/maintenance station data in the city where the scooter is running.
        """
        query = ''' query getStation($city_id: Int, $type: String) {
            getStation(city_id: $city_id, type: $type) {
                id
                latitude
                longitude
            }
        } '''

        payload = {
            'query': query,
            'variables': {
                'city_id': self.city["id"],
                'type': station_type
            }
        }

        response = requests.post(self._URL, json = payload, headers = self._HEADERS)
        print(response.json())
        # return the response.join() data


    def create_scooter(self) -> None:
        """ Create a new scooter."""

    def create_user(self) -> None:
        """ Create a new user."""
