#!/usr/bin/python3

"""
Mainprogram for scooter simulation
"""


from datetime import datetime
import time
from src.scooter import Scooter
from src.api import ApiData
from main import Handler



class Simulation():
    """ Simulation class """

    # saves scooter id in an array
    _scooter_id = []

    # saves station in an array
    _station = []

    # saves user id in an array
    _user_id = []

    # saves city info in an array
    _city_data = []


    def __init__(self):
        """ Initialize class """
        self.scooter = Scooter()
        self.handler = Handler()
        self.api = ApiData(1)


    def move(self) -> None:
        """ Moves scooters around the cities. Simulation time is 2 minutes. """
        end_time = time.time() + 120    # 2 minutes

        print("\nStep 2 - Moving scooters . . . . . . . .")

        while time.time() <= end_time:
            count = 0

            while count < len(self._scooter_id):
                data = self.api.get_scooter_data(self._scooter_id[count])

                self.scooter.add_scooter_to_dict(data)
                self.scooter.add_city_to_dict(self._city_data[count])

                count = self.run(count)

                count += 1
                time.sleep(0.001)


    def delete_and_remove(self, count) -> None:
        """ Removes a specific element from the list and stop the scooter """
        self.end(count)

        del self._scooter_id[count]
        del self._station[count]
        del self._user_id[count]
        del self._city_data[count]
    

    def run(self, count: int) -> int:
        """
        Checks if the scooter is inside the city and check battery level, if TRUE
        the scooter will be returned otherwise the scooter will continue moving.
        """
        id = self._scooter_id[count]

        if self.scooter.check_scooter_in_city() is False:
            print("\nScooter {} is outside of the city\n".format(id))
            print("Scooter {} will be returned.".format(id))

            self.delete_and_remove()
            count -= 1
        elif self.scooter.check_battery():
            print("\n\033[1;31m*\033[1;0m Low battery!! the scooter {} needs to be charged.".format(id))
            print("Scooter {} will be returned.".format(id))

            self.delete_and_remove()
            count -= 1
        else:
            self.scooter.change_location()
            self.scooter.move_scooter()
            self.api.update_rented_scooter()

        return count


    def end(self, count):
        """
        Scooter will be checked if it's outside the city/has low battery level or need
        meantience. The scooter will be returned and the log/payment/account will be uppdated.
        """
        self.api.station = self._station[count]
        self.handler.api = ApiData(self._user_id[count])

        self.handler.end_rental()


    def return_scooters(self):
        """ All scooters will be returned when simulation time ends. """
        count = 0

        print("\nStep 3 - Returning scooters . . . . . . . .")
        print("\nThe simulation has finished, the scooters will be returned.\n")

        while count < len(self._scooter_id):
            data = self.api.get_scooter_data(self._scooter_id[count])

            self.scooter.add_scooter_to_dict(data)
            self.scooter.add_city_to_dict(self._city_data[count])
            self.end(count)

            count += 1
            time.sleep(0.001)


    def main(self, total:int):
        """ Start simulation program. """
        print("\n************ Welcome to Scooter simulation program **************\n")
        print("\nThe simulation takes around 3 minutes, do not try to break/stop the program.\n")
        print("\nStep 1 - Renting scooters . . . . . . . .")

        current = datetime.now().time().strftime("%H:%M:%S")
        self.handler.start_time = [int(current[:2]), int(current[3:5]), int(current[6:8])]
        count = 1

        # user id 6 means customer id 1, start counting from 6
        user = 6 

        while count <= total:
            data = self.api.get_scooter_data(scooter_id = count)

            if self.scooter.check_scooter_status(data):
                # get city
                city = self.api.get_city_data()
                self._city_data.append(city)
                self._scooter_id.append(count)

                # create log/payment and update customer's account
                self._user_id.append(user)
                self.api.user_id = str(user)

                self.api.rent_scooter()
                self._station.append(self.api.station)

                user += 1
            else:
                print("\n\033[1;31m*\033[1;0m Scooter {} is not available.\n".format(count))

            count += 1

        self.move()
        self.return_scooters()



if __name__ == "__main__":
    Simulation().main(1000)