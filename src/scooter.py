#!/usr/bin/python3

"""
File for handling scooter data.

Scooter's status id:
1- Available
2- Unavailable
3- Maintenance
4- Charging
7- Running

scooter's data
data = {
    "id": "1",              # scooter id (str)
    "lat": 59.174586,       # coordinates (float)
    "lon": 17.602334,       # coordinates   (float)
    "speed": 0,             # km/h  (int)
    "battery": 0,           # % (int)
    "status": "7"           # status id (str)
    "station": "1"          # station id (str)
}

city's data
city = {
    "id": "2",          # citys id (str)
    "area": 25.84,      # km²   (float)
    "lat": 59.19554,    # coordinates (float)
    "lon": 17.62525     # coordinates (float)
}
"""

import math
import random
import re
from geopy.distance import geodesic, distance



class Scooter():
    """ Scooter class """

    # scooter's data
    data = {}

    # city's data
    city = {}

    # scooter's new coordinates
    location = ""


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


    def check_scooter_status(self, scooter: dict) -> bool:
        """
        Returns true if the scooter is available and adds the scooter's
        data to data dictionary.
        """
        if scooter["status"]["status"] == "Available":
            self.add_scooter_to_dict(scooter)
            return True
        return False


    def add_scooter_to_dict(self, scooter: dict) -> None:
        """ Adds scooter's data to the dictionary. Status id 7 means 'Running'. """
        self.data["id"] = scooter["id"]
        self.data["lat"] = float(scooter['latitude'])
        self.data["lon"] = float(scooter['longitude'])
        self.data["speed"] = int(scooter['speed'])
        self.data["battery"] = int(scooter['battery'])
        self.data["status"] =  "7"


    def add_city_to_dict(self, city: dict):
        """ Adds scooter's data to the dictionary. Status id 7 means 'Running'. """
        self.city["id"] = city["id"]
        self.city["lat"] = float(city['latitude'])
        self.city["lon"] = float(city['longitude'])
        self.city["area"] = float(city['area'])


    def move_scooter(self) -> None:
        """
        Move the scooter from one position to another and reduce battery level.
        Max scooter speed is 20km/h.
        """
        # get random speed
        speed = random.randrange(1, 21)
        points = re.split("Point|, ", self.location)

        self.data["lat"] = float(points[1][1:])
        self.data["lon"] = float(points[2])
        self.data["speed"] = speed
        self.data["battery"] -= 1


    def change_location(self) -> None:
        """
        Get random location inside the city zone.
        Speed = distance ÷ time => distance = speed * time
        Bearing in degrees: North: 0, East: 90, South: 180, West: 270.
        """
        # 5 seconds is sleep time, scooter moves every 5 seconds
        # but for better simulation I increase it to 15 seconds
        distance_km = self.data["speed"] * (15 / 3600)

        # get random position
        bearing = random.randint(0, 3)
        degrees = [0, 90, 180, 270]

        new_location = repr(distance(kilometers = distance_km).destination(
            (self.data["lat"], self.data["lon"]),
            bearing = degrees[bearing])
        )

        self.location = new_location


    def stop_scooter(self, status = "7") -> None:
        """ Stop the scooter from running. Change status and speed. """
        self.data["status"] = status
        self.data["speed"] = 0


    def check_battery(self) -> bool:
        """ Returns True if the battery level < 20%. """
        return self.data["battery"] < 20


    def move_to_station(self, station: dict) -> None:
        """ Move the scooter to charging/maintenance station. """
        self.data["lat"] = float(station["latitude"])
        self.data["lon"] = float(station["longitude"])
        self.data["station"] = station["id"]


    @staticmethod
    def check_maintenance() -> bool:
        """
        Returns true if the random number is 1 otherwise False, since scooters are not
        real, the maintenance check will be randomly.
        The probability that the scooter receives maintenance is 10%.
        """
        probability = random.randint(1, 10)
        return probability == 1


    def check_scooter_in_city(self) -> bool:
        """
        Check if scooter is inside the city zone. If the distance between
        two points 'city center and scooter' <= circle radius return True.
        """
        # Circle Area = pi * r^2 => r^2 = A/pi
        radius = math.sqrt((self.city["area"] / math.pi))
        scooter = (self.data["lat"], self.data["lon"])
        city = (self.city["lat"], self.city["lon"])

        calculate = geodesic(scooter, city).km

        if calculate <= radius:
            return True
        return False
