#!/usr/bin/python3

"""
Mainprogram for scooter simulation
"""


import time
from src.scooter import Scooter
from src.api import ApiData
from main import Handler



class Simulation():
    """ Simulation class """

    # saves scooter id in an array
    _scooter_id = []

    # saves log id in an array
    _log_id = []

    # saves station id in an array
    _station_id = []

    # saves city info in an array
    _city_data = []

    def __init__(self):
        """ Initialize class """
        self.scooter = Scooter()
        self.handler = Handler()
        self.api = ApiData(1)


    def move(self) -> None:
        """ Move scooters around the cities. Simulation time is 2 minutes. """
        end_time = time.time() + 120    # 2 minutes

        while time.time() <= end_time:
            count = 0

            while count < len(self._scooter_id):
                id = self._scooter_id[count]
                data = self.api.get_scooter_data(scooter_id = id)

                self.scooter.add_scooter_to_dict(data)
                self.scooter.add_city_to_dict(self._city_data[count])
                self.scooter.set_station_id(self._station_id[count])


                self.run(count, id)
                count += 1
                time.sleep(0.001)


    def run(self, count: int, id: int):
        """
        Check if the scooter is inside the city and check battery level, if TRUE
        the scooter will be returned otherwise the scooter will continue moving.
        """
        if self.scooter.check_scooter_in_city() is False:
            print("\nScooter {} is outside of the city\n".format(id))
            print("Scooter {} will be returned.".format(id))

            self.end(count)

            del self._scooter_id[count]
            del self._log_id[count]
            del self._station_id[count]
            del self._city_data[count]

            count -= 1
        elif self.scooter.check_battery():
            print("\n\033[1;31m*\033[1;0m Low battery!! the scooter {} needs to be charged.".format(id))
            print("Scooter {} will be returned.".format(id))

            self.end(count)

            del self._scooter_id[count]
            del self._log_id[count]
            del self._station_id[count]
            del self._city_data[count]

            count -= 1
        else:
            self.scooter.change_location()
            self.scooter.move_scooter()
            self.api.update_scooter()


    def end(self, count):
        """
        Scooter will be checked if it's outside the city/has low battery level or need
        meantience. The scooter will be returned and the log will be uppdated.
        """
        self.handler.end_rental()
        self.api.update_scooter()

        self.api.log_id = self._log_id[count]
        self.api.update_log()


    def return_scooters(self):
        """ All scooters will be returned when simulation time ends. """
        count = 0

        while count < len(self._scooter_id):
            id = self._scooter_id[count]
            data = self.api.get_scooter_data(scooter_id = id)

            self.scooter.add_scooter_to_dict(data)
            self.scooter.add_city_to_dict(self._city_data[count])
            self.scooter.set_station_id(self._station_id[count])

            self.end(count)
            time.sleep(0.001)
            count += 1


    def main(self, total:int):
        """ Start simulation program. """
        print("\n************ Welcome to Scooter simulation program **************\n")
        print("\nSimulation time is 2 minutes, do not try to break/stop the program.\n")

        all_customers = self.api.get_all_customers()

        count = 1
        customer = 0

        while count <= total:
            data = self.api.get_scooter_data(scooter_id = count)

            if self.scooter.check_scooter_status(data):
                city = self.api.get_city_data()
                self.scooter.add_city_to_dict(city)
                self._city_data.append(city)
                self._scooter_id.append(count)

                # create log
                self.api.user_id = str(all_customers[customer]["id"])
                self.api.create_log()
                self._log_id.append(self.api.log_id)

                ## get station
                zone = self.scooter.get_zone_id()
                station = self.api.get_station(zone)
                self._station_id.append(station)

                customer += 1
            else:
                print("\n\033[1;31m*\033[1;0m Scooter {} is not available.\n".format(count))

            count += 1

        self.move()
        self.return_scooters()



if __name__ == "__main__":
    Simulation().main(497)