class ChainHashTable:
    """
    This class is a hash table used to store package data.

    Attributes
    ----------
    table : list[list[package obj]
        The outer list of the hash table
    hash : lambda
        The hash function for the hash table
    buckets : int
        The number of buckets in the hash table (default is 10)

    Methods
    -------
    insert(key, item)
        Inserts a new package object into the hash table

    search(key)
        Searches for a package object in the hash table

    remove(key)
        Removes a package object from the hash table

    deliver(key)
        Changes a package object's status to True

    display(key)
        Displays information about one or all packages
    """

    #O(1)
    def __init__(self, buckets=10):
        """
        Parameters
        ----------
        buckets : int
            The number of buckets for the hash table
        """
        self.table = []
        self.hash = lambda x: x % buckets
        for n in range(buckets):
            self.table.append([])

    #O(1)
    def insert(self, key, item):
        """
        Inserts a new package object into the hash table.

        Parameters
        ----------
        key : int
            The unique key of the package object

        item: Package
            The new package object to be inserted
        """
        table_ix = self.hash(key)
        self.table[table_ix].append(item)

    #O(n)
    def search(self, key):
        """
        Searches for a package object in the hash table.

        Parameters
        ----------
        key : int
            The unique key of the package object

        Returns
        ----------
        Package
            The package object that matches the unique key
        """
        table_ix = self.hash(key)
        for item in self.table[table_ix]:
            if item.id == key:
                return item
        return

    #O(n)
    def remove(self, key):
        """
        Removes a package object from the hash table.

        Parameters
        ----------
        key : int
            The unique key of the package object
        """
        table_ix = self.hash(int(key))
        item = self.search(key) #O(n)
        if item:
            self.table[table_ix].remove(item)

    #O(n)
    def deliver(self, key, time, truck_num):
        """
        Represents a package object being delivered and changes its status.

        Parameters
        ----------
        key : int
            The unique key of the package object

        time : datetime.time
            The time that the package was delivered

        truck_num : int
            The id of the truck that delivered the package
        """
        item = self.search(key) #O(n)
        if item:
            item.status = "delivered at " + str(time) + ' (Truck ' + str(truck_num) + ')'

    #O(n)
    #Where n = the number of items in the hash table
    def display(self, keys):
        """
        Displays a given package's ID and status or displays all packages

        Parameters
        ----------
        keys : list[int]
            The list of keys to display sttatus of
        """
        for key in keys:
            item = self.search(key)
            if item:
                tab1 = '\t'
                tab2 = '\t'
                time = item.time_left
                if item.id < 10: #improves formatting for single digit ids
                    tab1 += '\t'
                if 'delivered' not in item.status: #improves formatting for shorter statuses
                    tab2 += '\t\t'
                    if item.status == 'at the hub': #adds more tabs for the shortest status
                        tab2 += '\t'
                if not time: #if the package has not left the hub
                    time = 'N/A'
                print('Package ID: ', item.id, tab1 + 'Delivery Status: ', item.status,
                      tab2 + 'Time Left Hub:', time)