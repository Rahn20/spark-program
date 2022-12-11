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
        self._thread = Thread(target=self.run, name="Update api/move scooter")


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
            if self._running:
                # update API/ move scooter
                time.sleep(5)


    def check_battery(self) -> None:
        """ Check battery level, if battery level is less than 20% print warning message."""

    def start_scooter(self) -> None:
        """ Move the scooter to a random location. """
        self._running = True

        #check battery level

    def stop_running(self) -> None:
        """ Stop the scooter. """
        if self._running is True:
            self._running = False


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


    def get_scooter_info(self):
        """ Get the scooter information. """
        if self._running:
            print("\nScooter is running.")
        else:
            print("\nScooter is in sleep mode.")

        print(self.scooter.__str__())
        print("Rent time: " + str(self.rental_time()))


    def return_scooter(self):
        """ Stop the rental and leave the scooter. """
        ## Stop thread
        self._return = True
        self._running = False
        self._thread.join()

        # update log (API)
        # update scooter (API)
        sys.exit()


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

            ## start a Thread
            self._thread.start()
            self.rent_scooter()

        except ValueError:
            print("\nScooter id must be a number.")


if __name__ == "__main__":
    Handler().main()
