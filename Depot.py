import datetime
import sys

import HashTable
import Truck
import Distance
import Package


class Depot:
    # Constructor
    def __init__(self, packages: HashTable.ChainingHashTable):
        # Truck capacity is 16
        self.packages = packages
        self.local_time = 8
        self.truck_one = Truck.Truck(truck_id=1)
        self.truck_one.time_departed = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)
        self.truck_two = Truck.Truck(truck_id=2)
        self.truck_two.time_departed = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)
        self.distance_class = Distance.Distance()
        packages_to_deliver_truck_one = (1, 4, 7, 13, 14, 15, 16, 19, 20, 21, 27, 29, 34, 35, 39, 40)
        self.load_packages(self.truck_one, *packages_to_deliver_truck_one)
        packages_to_deliver_truck_two = (3, 5, 6, 8, 10, 17, 18, 22, 25, 26, 30, 31, 32, 36, 37, 38)
        self.load_packages(self.truck_two, *packages_to_deliver_truck_two)

    def find_optimal_path(self, truck: Truck) -> tuple[int, float, Package]:
        """
        This function iterates through the packages that a truck has and attempts to find the package with the shortest
        distance from its current position.  It also takes into account if a package should be prioritized such as a
        package that needs to be delivered before a deadline.  It then returns the index of the package it should go to,
        the distance to that package, and the optimal package itself
        :param truck: the truck to check the packages of.
        :return: a tuple of int: (optimal_package_index), float: (shortest_distance), Package: (optimal_package)
        """
        shortest_distance = sys.maxsize
        optimal_package = None
        optimal_package_index = 0
        for p in truck.packages:
            address_id = self.distance_class.address_lookup(address=p.address)
            distance_to_target = float(self.distance_class.get_distance_to(truck.current_index, address_id))
            if 'EOD' not in p.deadline:
                if optimal_package is None:
                    pass
                else:
                    delivery_time = p.deadline.split(" ")[0]
                    optimal_delivery_time = optimal_package.deadline.split(" ")[0]
                    if 'EOD' in optimal_package.deadline or should_update_optimal_package(
                            time_one=optimal_delivery_time,
                            time_two=delivery_time,
                            distance_to_target=distance_to_target,
                            shortest_distance=shortest_distance):
                        shortest_distance = distance_to_target
                        optimal_package = p
                        optimal_package_index = address_id
            if distance_to_target < shortest_distance:
                if optimal_package is None or 'EOD' in optimal_package.deadline:
                    shortest_distance = distance_to_target
                    optimal_package = p
                    optimal_package_index = address_id
        return optimal_package_index, shortest_distance, optimal_package

    def deliver_next_package(self, truck: Truck) -> None:
        """
        Delivers the next optimal package in the list of packages from the truck, updates the current index/location of
        the truck, updates the total miles travelled by the truck, and delivers/unloads the package from the truck
        :param truck: the truck to deliver the next package of
        :return: None
        """
        shortest_destination = self.find_optimal_path(truck=truck)
        package = shortest_destination[2]
        if package is None:
            return None
        self.packages.lookup(str(package.package_id)).status = Package.DeliveryStatus.DELIVERED
        truck.current_index = shortest_destination[0]
        truck.miles_travelled += shortest_destination[1]
        self.packages.lookup(str(package.package_id)).delivered_timestamp = truck.get_current_time()
        truck.unload_truck(shortest_destination[2])
        return None

    def deliver_packages(self, truck: Truck) -> None:
        """
        Iterates through the list of packages that the truck has and delivers all of them as long as it has more to
        deliver
        :param truck: the truck to deliver packages from
        :return: None
        """
        for i in range(len(truck.packages)):
            self.deliver_next_package(truck)
        return None

    def return_to_depot(self, truck: Truck) -> None:
        """
        Returns the truck to the depot, updates the miles it takes to get there and then loads the truck with more
        packages
        :param truck: the truck to return to the depot
        :return: None
        """
        address_id = self.distance_class.address_lookup(address="4001 South 700 East")
        distance_to_target = float(self.distance_class.get_distance_to(truck.current_index, address_id))
        truck.current_index = 0
        truck.miles_travelled += distance_to_target
        final_packages = (2, 9, 11, 12, 23, 24, 28, 33)
        if truck.get_current_time() > datetime.datetime.today().replace(hour=10, minute=20, second=0, microsecond=0):
            # Current time is after 10:20, changing the address of package number 9
            self.packages.lookup("9").address = "410 S State St"
        self.load_packages(self.truck_two, *final_packages)
        return None

    def display_total_miles_traveled(self) -> float:
        """
        Returns the total amount of miles traveled by truck one and two
        :return: float the total amount of miles traveled
        """
        total_miles = self.truck_one.miles_travelled + self.truck_two.miles_travelled
        return total_miles

    def load_packages(self, truck: Truck, *package_ids: int):
        """
        Loads packages given their id's onto the specified truck
        :param truck: the truck to load the packages on
        :param package_ids: the package ids to load onto the truck
        :return: None
        """
        for i in package_ids:
            package = self.packages.lookup(str(i))
            if package is not None:
                truck.load_truck(package)
                self.packages.lookup(str(i)).status = Package.DeliveryStatus.ON_TRUCK
                self.packages.lookup(str(i)).loaded_timestamp = truck.get_current_time()
            else:
                print("None package")


def should_update_optimal_package(time_one: str, time_two: str, distance_to_target: float,
                                  shortest_distance: float) -> bool:
    """
    Checks to see if a package with a deadline needs to be updated.  Checks to see if the delivery times are the same,
    and if they are it will check which one is closer, otherwise it will prioritize the package that needs to be
    delivered first
    :param time_one: the current optimal package delivery time
    :param time_two: the package being tested delivery time
    :param distance_to_target: the distance to the tested package
    :param shortest_distance: the current shortest distance
    :return: bool if we should update the current optimal package or not
    """
    # If optimal time is less than current package_time we should update.
    optimal_package_time = datetime.datetime.strptime(time_one, "%H:%M")
    testing_package_time = datetime.datetime.strptime(time_two, "%H:%M")
    if optimal_package_time == testing_package_time:
        return distance_to_target < shortest_distance
    return optimal_package_time > testing_package_time
