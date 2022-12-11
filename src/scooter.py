#!/usr/bin/python3

""" File for handling scooter data with Scooter class. """

import random


class Scooter():
    """ Scooter class """

    ## scooters data
    data = {
        "id": 0,
        "lat": 0,
        "lon": 0,
        "speed": 0,
        "battery": 0,
        "status": ""
    }


    def __init__(self) -> None:
        """ Initialize class """


    def __str__(self) -> str:
        """ Returns scooters data """
        return "Scooter id: {0}\nLocation: {1}, {2}\nSpeed: {3}km/h\nBattery: {4}%".format(
            self.data["id"],
            self.data["lat"],
            self.data["lon"],
            self.data["speed"],
            self.data["battery"],
        )


    def move_scooter(self) -> None:
        """
        Move the scooter from one position to another and reduce battery level.
        Max scooter speed is 20km/h.
        """
        speed = random.randrange(1, 21)

        self.data["speed"] = speed


    def stop_scooter(self) -> None:
        """ Stop the scooter from running. """
        self.data["speed"] = 0


    def get_battery_level(self) -> int:
        """ Returns battery level """
        return self.data["battery"]


    def change_position(self):
        """ Change scooter's position. """
