import datetime

import Depot
import HashTable
import Package

# Initialize hash table
myHash = HashTable.ChainingHashTable()
# Load the package data into the hashtable
Package.load_package_data("data/packages.csv", myHash)
# Initialize the depot with the hashtable containing the packages
depot = Depot.Depot(packages=myHash)
# Deliver packages on truck one
depot.deliver_packages(depot.truck_one)
# Deliver packages on truck two
depot.deliver_packages(depot.truck_two)
# Returns truck two to the depot to pick up the rest of the packages
depot.return_to_depot(depot.truck_two)
# Deliver the rest of the packages on truck two
depot.deliver_packages(depot.truck_two)


def print_package_info(timestamp_to_check: datetime.datetime, package_to_check: Package):
    """
    Prints the package information for the specific package or timestamp requested by the user in the cli interface
    :param timestamp_to_check:  the timestamp the user wishes to check on
    :param package_to_check:  the package the user wishes to check on
    :return: None
    """
    package_message = f"Package ID: {package_to_check.package_id}, Address: {package_to_check.address}, " \
                      f"Deadline: {package_to_check.deadline}, Weight: {package_to_check.weight}, "
    if timestamp_to_check >= package_to_check.delivered_timestamp:
        # If the package is delivered.
        message_addition = f"Delivery status: {Package.DeliveryStatus.DELIVERED.value}, " \
                           f"Timestamp: {package_to_check.delivered_timestamp}"

        if 'EOD' in package_to_check.deadline:
            message_addition += f", Delivered on time."
        else:
            deadline_timestamp_string = package_to_check.deadline.split(" ")[0]
            date_now = datetime.datetime.now()
            deadline_timestamp = datetime.datetime.strptime(deadline_timestamp_string, "%H:%M").replace(
                year=date_now.year, month=date_now.month, day=date_now.day)
            print(deadline_timestamp)
            if package_to_check.delivered_timestamp < deadline_timestamp:
                message_addition += f", Delivered on time."
    else:
        # If package is not delivered.
        if package_to_check.loaded_timestamp > timestamp_to_check:
            # If the loaded time was later than the input time
            message_addition = f"Delivery status: {Package.DeliveryStatus.AT_HUB.value}"
        else:
            message_addition = f"Delivery status: {Package.DeliveryStatus.ON_TRUCK.value}"
    package_message += message_addition
    print(package_message)


def get_user_timestamp() -> datetime.datetime:
    """
    Gets the specific timestamp the user wishes to check and converts it into datetime
    :return: datetime that is provided by the user
    """
    user_time_input = input("Please input a time to check: HH:MM:SS\n")
    if user_time_input.count(':') != 2:
        print("Please input a valid time.")
        return get_user_timestamp()
    else:
        (h, m, s) = user_time_input.split(":")
        return datetime.datetime.today().replace(hour=int(h), minute=int(m), second=int(s), microsecond=0)


if __name__ == '__main__':
    shouldExit = False
    print("Welcome to the Package Delivery System!")
    # Shows how many miles it took to complete the route
    while not shouldExit:
        # The interface the user will interact with
        result = input("Please select an option \n"
                       + "1. Get info for all packages at a specific time.\n"
                       + "2. Get info for a specific package.\n"
                       + "3. Display total mileage travelled by all trucks.\n"
                       + "4. Exit.\n")
        # If the result is one, print the information for all packages at the specified timestamp
        if result == '1':
            timestamp = get_user_timestamp()
            # The range of all 40 packages
            for i in range(41):
                current_package = depot.packages.lookup(str(i))
                if current_package is not None:
                    print_package_info(timestamp_to_check=timestamp, package_to_check=current_package)
            print("")
        # If the result is two, print the information for the specific package id at the specified timestamp
        elif result == '2':
            package_id = input("Please input a package id to check: ")
            package = depot.packages.lookup(package_id)
            timestamp = get_user_timestamp()
            if package is None:
                print("Invalid package id.")
            else:
                print_package_info(timestamp_to_check=timestamp, package_to_check=package)
        # If the result is three, print the total miles traveled by the trucks
        elif result == '3':
            print(f'Route was completed in: {round(depot.display_total_miles_traveled(), 2)} miles.')
        # If the result is three, exit the program.
        elif result == '4':
            print("Thanks for using WGUPS.")
            shouldExit = True
        #  If an invalid option was selected, print invalid input
        else:
            print("Invalid input.")
