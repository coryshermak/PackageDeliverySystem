from Package import Package

import datetime


class Truck:
    # Constructor
    def __init__(self, truck_id: int):
        self.truck_id = truck_id
        self.capacity = 16
        self.mph = 18
        self.packages = []
        self.miles_travelled = 0
        self.current_index = 0
        self.time_departed = datetime.datetime.now()

    def get_hours_driven(self) -> float:
        """
        Calculates the amount of hours driven based on how many miles were travelled and how fast the truck was moving.
        :return: the float value of the hours driven of the truck
        """
        return self.miles_travelled / self.mph

    def get_current_time(self) -> datetime:
        """
        Calculates the current time of the truck based on how many hours were driven after the initial departure from
        the depot
        :return: the datetime value of the current time driven
        """
        return self.time_departed + datetime.timedelta(hours=self.get_hours_driven())

    def is_full(self) -> bool:
        """
        Checks to see if the truck is full on capacity of packages.
        :return: bool value of whether the truck is full of packages or not
        """
        return len(self.packages) >= self.capacity

    def load_truck(self, *packages: Package) -> bool:
        """
        Loads the truck with the provided packages if it is not already full on capacity
        :param packages: the packages to load the truck with.
        :return: bool value of whether the truck was able to load he packages or not.
        """
        if self.is_full():
            return False
        for p in packages:
            self.packages.append(p)
        return True

    def unload_truck(self, *packages: Package) -> None:
        """
        Unloads the truck with the provided packages
        :param packages: the packages to unload from the truck
        :return: None
        """
        for p in packages:
            self.packages.remove(p)
        return None
