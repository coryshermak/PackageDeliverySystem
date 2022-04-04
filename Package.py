from enum import Enum
import csv


class DeliveryStatus(Enum):
    """
    DeliveryStatus Enum to help keep track of the status of the package.
    """
    AT_HUB = "At Hub"
    ON_TRUCK = "On Truck"
    DELIVERED = "Delivered"


class Package:
    """
    Constructor
    """

    def __init__(self, package_id: int, address, deadline, city, state, zipcode, weight, notes, status):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.notes = notes
        self.status = status
        self.loaded_timestamp = None
        self.delivered_timestamp = None

    # String operator overload
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.package_id, self.address, self.deadline, self.city, self.zipcode, self.weight, self.status.value,
            self.delivered_timestamp)


def load_package_data(file_name, my_hash):
    """
    Loads package data from the packages.csv provided
    :param file_name: the file to read data from
    :param my_hash:  the has table to store data in
    :return: None
    """
    with open(file_name) as packages:
        read_csv = csv.reader(packages, delimiter=',')
        for row in read_csv:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]
            status = DeliveryStatus.AT_HUB

            p = Package(package_id=package_id, address=address, city=city, state=state, zipcode=zipcode,
                        deadline=deadline, weight=weight, notes=notes, status=status)
            # Enter insert loop
            my_hash.insert(str(package_id), p)
