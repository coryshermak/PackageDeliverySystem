import csv


class Distance:
    """
    Constructor - reads distance data from distances.csv and address data from addresses.csv that were provided
    """

    def __init__(self):
        dicts = {}
        with open("data/distances.csv") as distances:
            distance_lists = list(csv.reader(distances, delimiter=','))
        with open("data/addresses.csv") as addresses:
            reader = csv.DictReader(addresses, delimiter=',')
            address_lists = list(csv.reader(addresses, delimiter=','))
        for i in range(len(address_lists)):
            current = address_lists[i]
            key = current[2]
            value = current[0]
            dicts[key] = int(value)
        self.distances = distance_lists
        self.addresses = address_lists
        self.dicts = dicts

    def address_lookup(self, address: str) -> int:
        """
        Looks up an address given a string and converts it into the addresses' id that was provided
        :param address: the address of type string to lookup
        :return: the int value of the address provided
        """
        return self.dicts.get(address)

    def get_distance_to(self, row, col) -> float:
        """
        Gets the distance from one location to the next location, useful for knowing the distance between two points
        :param row: the row to check
        :param col: the column to check
        :return: the float value of the distance to the next location based on the current location.
        """
        distance = self.distances[row][col]
        if distance == '':
            distance = self.distances[col][row]
        return float(distance)
