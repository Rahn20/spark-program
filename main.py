#!/usr/bin/python3

""" Main file for scooter program with Handler class. """

import sys
import inspect
import time
from threading import Thread
from datetime import datetime, timedelta

from src.api import ApiData
from src.scooter import Scooter


class Handler():
    """ Handler class """

    ## menu options
    _OPTIONS = {
        "1": "start_scooter",
        "2": "stop_running",
        "3": "get_scooter_info",
        "4": "return_scooter",
        "5": "charge_scooter",
    }

    ## scooter status
    _running = False

    ## Leave the scooter, stop the thread
    _return = False

    ## start renting time, a list of integers [H:M:S]
    _start_time = None


    def __init__(self) -> None:
        """ Initialize class """
        self.scooter = Scooter()
        self.api = ApiData(user_id = 1)   ## user id (random user)

        ## create a Thread
        self._thread = Thread(target=self.run, name="Move scooter")


    def _get_method(self, method_name):
        """ Uses function getattr() to dynamically get value of an attribute. """
        return getattr(self, self._OPTIONS[method_name])


    def _print_menu(self) -> None:
        """ Prints options for the program. """
        menu = ""

        for key in sorted(self._OPTIONS):
            method = self._get_method(key)
            docstring = inspect.getdoc(method)

            menu += "{choice}: {explanation}\n".format(
                choice = key,
                explanation = docstring
            )

        print(chr(27) + "[2J" + chr(27) + "[;H")
        print(menu)


    def run(self) -> None:
        """ Start a Thread. """
        while True:
            if self._return:
                break
            if self.scooter.check_scooter_in_city() is False:
                print("\nScooter is outside of the city")
                print("You can't use the scooter anymore. Press 4 to cancel the rental.")

                self.stop_running()
                time.sleep(10)
            elif self._running:
                self.battery_check()
                time.sleep(5)


    def battery_check(self) -> None:
        """ Check battery level, if battery < 20% print warning message and stop the scooter. """
        if self.scooter.check_battery():
            self.stop_running()
            print("\n\033[1;31m*\033[1;0m Low battery!! the scooter needs to be charged.")
        else:
            self.scooter.change_location()
            self.scooter.move_scooter()

            ## update API
            #self.api.update_scooter()


    def start_scooter(self) -> None:
        """ Move the scooter to a random location if battery > 20%. """
        if self.scooter.check_battery():
            print("\n\033[1;31m*\033[1;0m Low battery!! the scooter needs to be charged.")
            print("\nPress 4 to end the rental and leave the scooter at charging station.")
            print("Or you can press 5 to fully charge the scooter and end the rental.")
        else:
            self._running = True


    def stop_running(self) -> None:
        """ Stop the scooter. """
        if self._running is True:
            self._running = False
            self.scooter.stop_scooter()

            ## update API
            #self.api.update_scooter()


    def rental_time(self) -> timedelta:
        """ Returns the time the scooter has been rented by a user. """
        current = datetime.now().time().strftime("%H:%M:%S")

        current_time = timedelta(
            hours = int(current[0:2]),
            minutes = int(current[3:5]),
            seconds=int(current[6:8])
        )

        start_time = timedelta(
            hours = self._start_time[0],
            minutes = self._start_time[1],
            seconds = self._start_time[2]
        )

        return current_time - start_time


    def get_scooter_info(self) -> None:
        """ Get the scooter information. """
        if self._running:
            print("\nScooter is running.")
        else:
            print("\nScooter is in sleep mode.")

        print(self.scooter.__str__())
        print("Rent time: " + str(self.rental_time()))


    def charge_scooter(self):
        """Charge the scooter and end the rental. """
        ## Stop thread
        self._return = True
        self._running = False
        self._thread.join()

        ## Fully charges the battery and leave it at the charging Station
        #charging = self.api.get_station("Charging Station")

        self.scooter.data["battery"] = 100
        self.scooter.stop_scooter("available")
        #self.scooter.move_to_station(charging)

        ## update API
        #self.api.update_scooter()
        #self.api.update_log()
        #self.api.remove_user_connection()
        sys.exit()


    def return_scooter(self):
        """ Stop the rental and leave the scooter. """
        ## Stop thread
        self._return = True
        self._running = False
        self._thread.join()
        self.end_rental()

        #self.get_scooter_info()
        #print(self.scooter.data["status"])

        ## update API
        #self.api.update_scooter()
        #self.api.update_log()
        #self.api.remove_user_connection()
        sys.exit()


    def end_rental(self) -> None:
        """ Checks scooter's battery/maintenance/zone and stops the scooter. """
        if self.scooter.check_scooter_in_city() is False:
            self.scooter.stop_scooter("unavailable")
        elif self.scooter.check_battery():
            #charging = self.api.get_station("Charging Station")

            self.scooter.stop_scooter("charge")
            #self.scooter.move_to_station(charging)
        elif self.scooter.check_maintenance():
            #maintenance = self.api.get_station("Maintenance Station")

            self.scooter.stop_scooter("maintenance")
            #self.scooter.move_to_station(maintenance)
        else:
            self.scooter.stop_scooter("available")


    def rent_scooter(self):
        """ Print menu """
        while True:
            self._print_menu()
            choice = input("What do you want to do: ")

            try:
                self._get_method(choice.lower())()
            except KeyError:
                print("\nInvalid choice!")

            input("\nPress any key to continue ...")


    def main(self):
        """ Main method """
        try:
            print("\n************ Welcome to Scooter program **************\n")

            while True:
                scooter = int(input("Enter scooter id: "))

                if self.api.check_scooter_status(scooter):
                    current = datetime.now().time().strftime("%H:%M:%S")
                    self._start_time = [int(current[:2]), int(current[3:5]), int(current[6:8])]
                    break

                print("\n\033[1;31m*\033[1;0m Scooter is not available.\n")

            ## connect user and create log
            #self.api.connect_user()
            #self.api.create_log()
            #self.api.get_city_data()

            ## start a Thread
            self._thread.start()
            self.rent_scooter()

        except ValueError:
            print("\nScooter id must be a number.")


if __name__ == "__main__":
    Handler().main()
