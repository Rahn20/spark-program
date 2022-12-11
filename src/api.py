#!/usr/bin/python3

"""
url1: https://spark.isal.live/api/v1/
url2: http://localhost:1337/api/v1/
"""


#import requests
#import json
#from datetime import date, datetime

from src.scooter import Scooter


class ApiData(Scooter):
    """ Api data class """
    ## API url
    _URL = "http://localhost:1337/api/v1/"


    def __init__(self, user_id: int) -> None:
        """ Initialize class """
        super().__init__()
        self._user_id = user_id


    def check_scooter_status(self, scooter_id: int) -> bool:
        """
        Check scooter status. Returns true if the scooter is available
        and adds the scooter's data to data dictionary.
        """
        # 1- Get scooter's current data from API, use get_scooter_data()
        # 2- update self.data dict with scooters data
        self.data["id"] = scooter_id

        # TEST return true to view the menu in main
        return True


    def connect_user(self) -> None:
        """ Connect user to a scooter. """
        # scooter's id  self.data["id"]
        # uppdate API


    def remove_user_connection(self) -> None:
        """ Remove connection between user and scooter. """
        # scooter's id  self.data["id"]
        # uppdate API


    def get_scooter_data(self) -> dict:
        """ Get information about the scooter."""


    def get_user_data(self) -> dict:
        """ Get information about the user. """


    def update_scooter(self) -> None:
        """ Update api with scooter's new position, speed and battery level. """
        # push self.data to API


    def create_log(self) -> None:
        """ Create log. Data to be created is scooter's position, date/time and scooter/user id. """
        #today = date.today().strftime("%d/%m/%Y")           # dd/mm/YY
        #time = datetime.now().time().strftime("%H:%M:%S")   # h:m:s

        #scooter's id  self.data["id"]
        # API


    def update_log(self) -> None:
        """ Update log. Data to be updated is scooter's position and date/time. """
        #today = date.today().strftime("%d/%m/%Y")           # dd/mm/YY
        #time = datetime.now().time().strftime("%H:%M:%S")   # h:m:s

        #scooter's id  self.data["id"]
        # API


    def create_scooter(self) -> None:
        """ Create a new scooter."""

    def create_user(self) -> None:
        """ Create a new user."""
