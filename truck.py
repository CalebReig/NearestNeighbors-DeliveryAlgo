from datetime import timedelta, time, date, datetime
from graph_traversal import Graph

class Truck:
    """
    This class represents a truck that is able to load and deliver packages.

    Attributes
    ----------
    number : int
        The id of the truck
    time : datetime.time
        The relative current time of the truck. This is updated at each destination.
    to_time : datetime.time
        The time that the truck will give a status update
    mi_traveled : float
        The total miles traveled
    cargo : list[(int, str)]
        A list of package_ids with their destination for packages loaded on the truck
    hub : str
        The Hub that the truck is operating from
    destinations : list[str]
        A list of destinations the truck must travel to
    visited : list[list[str]]
        A list containing the paths that the truck took per trip
    trip_num : int
        The number of trips the truck took in a day minus 1
    at_hub : bool
        Indicated if the truck is currently at its hub

    Methods
    -------
    load_truck(package_ids, hash_table)
        Loads a number of packages onto the truck

    update_time(miles)
        Updates the relative current time of the truck

    update_cargo(hash_table, node)
        Updates the cargo of the truck while delivering packages

    deliver_cargo(graph, hash_table)
        Delivers loaded cargo to its relative address

    load_and_deliver(package_ids, hash_table, graph)
        Loads the truck with given packages and delivers them to their destinations

    display()
        Displays information about the truck object
    """

    def __init__(self, number, start_time):
        """
        Parameters
        ----------
        number : int
            The id of the truck
        start_time : datetime.time
            The time the truck will leave the hub
        """

        self.number = number
        self.time = start_time
        self.to_time = None
        self.mi_traveled = 0
        self.cargo = []
        self.hub = '4001 South 700 East'
        self.destinations = []
        self.visited = []
        self.trip_num = -1
        self.at_hub = True

    #O(n^2)
    def load_truck(self, package_ids, hash_table):
        """
        Loads a number of packages onto the truck.

        Parameters
        ----------
        package_ids : list[int]
            A list of package ids of packages to load on the truck
        hash_table : ChainHAshTable
            The hash table storing all package information
        """
        self.trip_num += 1
        self.visited.append([])
        for id in package_ids:
            package = hash_table.search(id)  # O(n)
            if package and (self.to_time != self.time):
                package.time_left = self.time
                package.status = "en route (Truck " + str(self.number) + ')'
                self.cargo.append((id, package.address))
            if package.address not in self.destinations:
                self.destinations.append(package.address)

    #O(1)
    def update_time(self, miles):
        """
        Updates the relative current time of the truck.

        Parameters
        ----------
        miles : float
            The number of miles the truck has traveled since the last time update

        Returns
        ----------
        bool
            Whether a status update needs to be provided to the user at the given time or not
        """
        time_taken = ((miles * 60) / 18)
        time_date = datetime.combine(date.today(), self.time) + timedelta(minutes=time_taken)
        if self.to_time:
            if time_date.time() > self.to_time:
                self.time = self.to_time
                return True
        self.time = time_date.time()
        return False

    #O(n^2)
    #Where n = the amount of packages in cargo
    def update_cargo(self, hash_table, node):
        """
        Updates the cargo of the truck while delivering packages.

        Parameters
        ----------
        hash_table : ChainHashTable
            The hash table storing all package information
        node : str
            The address that the truck is currently at
        """
        temp_cargo = self.cargo.copy()
        for i in range(len(temp_cargo)):
            package = temp_cargo[i]
            if package[1] == node:
                self.cargo.remove(package)
                hash_table.deliver(package[0], self.time, self.number) #O(n)

    #O(n^3)
    #Where n = the number of destinations that one truck must visit
    def deliver_cargo(self, graph, hash_table):
        """
        Delivers loaded cargo to its relative address.

        Parameters
        ----------
        graph : Graph
            The graph storing data about addresses
        hash_table : ChainHashTable
            The hash table storing all package information

        Returns
        ----------
        Null
        """
        #Sets reference variables
        ref_matrix = graph.matrix.copy()
        ref_places = graph.places.copy()
        num_dest = len(self.destinations)
        #Truck starts path at the hub
        curr_node = self.hub
        self.visited[self.trip_num].append(self.hub)
        #Truck leaves hub
        self.at_hub = False
        #Until all destinations are visited,
        #find the next nearest destination and deliver packages
        while len(self.visited[self.trip_num]) <= num_dest:  # O(n)
            next_dest, miles = graph.find_nearest_neighbor(curr_node)  # O(n)
            curr_node = next_dest
            sub_matrix = graph.create_partial_graph(self.destinations)  # O(n^2)
            graph = Graph(self.destinations.copy(), sub_matrix)
            if self.update_time(miles):
                return
            self.visited[self.trip_num].append(curr_node)
            self.destinations.remove(curr_node)  # O(n)
            self.mi_traveled += miles
            self.update_cargo(hash_table, curr_node)
        #The Truck travels back to the hub from its last destination
        hub_miles = ref_matrix[ref_places.index(curr_node)][ref_places.index(self.hub)]
        self.update_time(hub_miles)
        self.mi_traveled += hub_miles
        self.visited[self.trip_num].append(self.hub)
        self.at_hub = True

    #O(n^3)
    def load_and_deliver(self, package_ids, hash_table, graph):
        """
        Loads the truck with given packages and delivers them to their destinations.

        Parameters
        ----------
        package_ids : list[int]
            The list of package ids of packages to load and deliver
        hash_table : ChainHashTable
            The hash table storing all package information
        graph : Graph
            The graph storing data about addresses

        Returns
        ----------
        Null
        """
        if self.to_time and (self.time > self.to_time):
            return
        self.destinations = []
        self.load_truck(package_ids, hash_table)  # O(n^2)
        sub_matrix = graph.create_partial_graph(self.destinations + [self.hub])  # O(n^2)
        sub_graph = Graph(self.destinations + [self.hub], sub_matrix)
        self.deliver_cargo(sub_graph, hash_table)  # O(n^3)

    #O(n)
    #Where n is the number of trips the truck took
    def display(self):
        """
        Displays information about the truck object
        """
        print('================================================================')
        print('Truck ', self.number)
        if self.at_hub and len(self.visited) > 0:
            print('At the Hub, Finished Delivery of Trip', self.trip_num + 1, 'at:', self.time)
        elif self.at_hub:
            print('At the Hub, Has Not Started Delivery. Will Begin Delivery at:', self.time)
        else:
            print('On Trip', self.trip_num + 1, ', Current Time is:', self.time)
        print('================================================================')
        print('Visited Destinations:')
        for i, lst in enumerate(self.visited):
            if len(lst) > 1:
                print('Trip ', i + 1, ':', lst)
        print('Distance Traveled:', round(self.mi_traveled, 2), 'mi')

