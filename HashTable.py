class ChainingHashTable:
    # Constructor
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts or Updates a new package object into the hash table.
    def insert(self, key, item):  #
        # get the bucket list where the package will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for a package with a matching key in the hash table.
    # Returns the package if it is found otherwise will return None.
    def lookup(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Removes a package with a  matching key from the hash table.
    def remove(self, key):
        # get the bucket list where the package  will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # remove the package  from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                print(f"Removing {key} from hashmap")
                bucket_list.remove([kv[0], kv[1]])
