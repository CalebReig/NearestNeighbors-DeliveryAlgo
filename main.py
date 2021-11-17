"""
Created by: Caleb Reigada
Student ID: 001165112
Date:       10/13/2021



main

This python file contains functions to create and add package objects to a hash table,
calculate groups of packages to be loaded together (on a truck object) using a
psuedo-greedy algorithm, and functions to display application information to the user via
the CLI.
The functions used for package objects are below:

        * create_package - creates a single package object from a given string of values
        * insert_all_packages - inserts all package objects into a hash table

The functions used to group packages together into individual loads are below:

        * find_nearby_packages - given a list of packages, find other packages that are nearby
        * create_load - create a single group (or load) of packages to be delivered
        * create_all_loads - takes all packages and splits them into a number of loads

The functions used to display information to the user are below:

        * display_title - displays the title page on the CLI
        * get_inputs - prompts the user to input time and package ids
"""

from read_data import create_graph_and_places, read_package_data
from package import Package
from hash_table import ChainHashTable
from graph_traversal import Graph
from truck import Truck
from datetime import time

#O(1)
def create_package(package_str):
    """
    Creates a package object from a comma separated value string.

    Parameters
    ----------
    package_str : str
        A comma seperated value string of package attributes

    Returns
    ----------
    Package
        A new package object
    """
    package = Package(package_str[0], package_str[1], package_str[5], package_str[2],
                      package_str[4], package_str[6])
    return package

#O(n)
#Where n = the total number of packages
def insert_all_packages(packages, hash_table):
    """
    Creates package objects for all packages and inserts them into a hash table.

    Parameters
    ----------
    packages : list[str]
        A list of comma separated value strings representing package attributes

    hash_table : ChainHashTable
        A hash table that will store the package objects
    """
    for package in packages:
        pack_obj = create_package(package)
        hash_table.insert(pack_obj.id, pack_obj)

#O(n^2)
def find_nearby_packages(loc_type, locations, load, packages_all, hash_table, max_load_size=16):
    """
    Finds packages that are nearby each other given a list of locations to search.

    Parameters
    ----------
    loc_type : str
        A string indicating if the location is an address, zipcode or city
    locations : list[str]
        A list of locations of the current packages in the load
    load : list[int]
        The package ids of the current load
    packages_all : list[int]
        A list of all the available packages
    hash_table : ChainHashTable
        A hash table that will store the package objects
    max_load_size : int
        The maximum size of the load (default = 16)

    Returns
    ----------
    list[int]
        A list of package ids that are in the load
    list[int]
        A list of remaining packages
    """
    for package_id in packages_all:
        if len(load) < max_load_size:
            if package_id in load:
                packages_all.remove(package_id)
            else:
                package = hash_table.search(package_id) #O(n)
                if loc_type == 'address':
                    if package.address in locations:
                        load.append(package.id)
                        packages_all.remove(package_id)
                elif loc_type == 'zipcode':
                    if package.zipcode in locations:
                        load.append(package.id)
                        packages_all.remove(package_id)
                else:
                    if package.city in locations:
                        load.append(package.id)
                        packages_all.remove(package_id)

        else:
            break

    return load, packages_all

#O(n^2)
def create_load(packages_need, packages_all, hash_table):
    """
    Creates a group of packages to load onto a truck.

    The function tries to group all packages with the same address,
    zip code or of the same city.

    Parameters
    ----------
    packages_need : list[int]
        A list of package ids that need to be in the load regardless of their address
    packages_all : list[int]
        A list of all the available packages
    hash_table : ChainHashTable
        A hash table that will store the package objects

    Returns
    ----------
    list[int]
        A list of package ids that are in the load
    list[int]
        A list of remaining packages
    """
    load = packages_need.copy() #The packages on the load
    addresses = []
    zip_codes = []
    cities = []

    if len(load) == 0:
        load.append(packages_all[0])
        packages_all.remove(packages_all[0])

    for i in load:
        package = hash_table.search(i)
        if package.address not in addresses:
            addresses.append(package.address)
        if package.zipcode not in zip_codes:
            zip_codes.append(package.zipcode)
        if package.city not in cities:
            cities.append(package.city)


    load, packages_all = find_nearby_packages('address', addresses, load, packages_all, hash_table) #O(n^2)
    load, packages_all = find_nearby_packages('zipcode', zip_codes, load, packages_all, hash_table) #O(n^2)

    return load, packages_all


#O(k * n^2)
def create_all_loads(num_loads, packages_all, packages_need_lst, hash_table):
    """
    Creates a number of loads that places all packages given into different groups

    Parameters
    ----------
    num_loads : int
        The number of loads to group packages into
    packages_all : list[int]
        A list of all the available packages
    packages_need_lst : list[list[int]]
        A list of lists of package ids that need to be in the load regardless of their address
    hash_table : ChainHashTable
        A hash table that will store the package objects

    Returns
    ----------
    list[list[int]]
        A list of loads containing package ids
    """
    all_loads = []

    for lst in packages_need_lst:
        for package_id in lst:
            if package_id in packages_all:
                packages_all.remove(package_id)

    for i in range(num_loads):
        try:
            package_need = packages_need_lst[i]
        except:
            package_need = []
        if i == num_loads - 1: #If this is the last load
            try:
                room = 16 - len(package_need)
                load = package_need + packages_all[:room]
                packages_all = packages_all[room:]
            except:
                load = package_need + packages_all
                packages_all = []

        else:
            load, packages_all = create_load(package_need, packages_all, hash_table) #O(n^2)
        all_loads.append(load)

    if len(packages_all) > 0: #if there are still remaining packages that have not been loaded
        for load in all_loads:
            while len(load) < 16 and len(packages_all) > 0:
                load.append(packages_all[0])
                try:
                    packages_all = packages_all[1:]
                except:
                    packages_all = []
                    break

    return all_loads

#O(1)
def display_title():
    """
    This function displays the title and description of the application upon startup.
    """

    print("""
    ============================================================================
    |      Nearest Neighbor Graph Traversal Package Delivery Application       |
    ============================================================================
     This application simulates delivering packages at many different addresses 
     using up to 2 trucks that can each hold a maximum of 16 packages at once. 
     The package and address information used for this simulation is stored in 
     csv files that have been provided by WGU. The algorithm used to determine 
     the order in which addresses are chosen is the nearest neighbor algorithm 
     which has a big-O time complexity of O(n^2) and the algorithm used to group
     packages together in loads is a modified greedy algorithm with a big-O time
     complexity of O(n^2). The entire program has a big-O time complexity of 
     O(n^3) with a spacial complexity of O(n^2).
    
                            Created by: Caleb Reigada
                            Student ID: 001165112
                            Date:       10/13/2021
                            
    ============================================================================
    """)

    input("Press Enter to Begin\n")

#O(1)
def get_inputs(trucks):
    """
    Prompts the user to input a time and package ids they would like to see the status of.

    Parameters
    ----------
    trucks : list[Truck]
        A list of truck objects

    Returns
    ----------
    list[int]
        A list of package ids to check the status of
    datetime.time
        The time to provide a status update to the user
    """

    print('\nEnter a time to see the status of packages and trucks at that time. Ex: 8:00')
    print('You may leave this blank or input an invalid time to continue to the end of the day.')
    to_time = input('Enter the time here: ')
    try:
        to_hour = int(to_time.split(':')[0])
        to_minute = int(to_time.split(':')[1])
        to_time = time(to_hour, to_minute, 0)
        for truck in trucks:
            truck.to_time = to_time
    except:
        for truck in trucks:
            truck.to_time = None

    print('\nEnter the id or ids of packages you would like the status of separated by commas.')
    print('You may leave this blank or input an invalid ids to display all package statuses.')
    package_ids_raw = input('Enter the package id(s) here: ')

    try:
        package_ids = [int(x) for x in package_ids_raw.split(',')]
    except:
        package_ids = None

    return package_ids, to_time



if __name__ == '__main__':

    """
     This application simulates delivering packages at many different addresses 
     using up to 2 trucks that can each hold a maximum of 16 packages at once. 
     The package and address information used for this simulation is stored in 
     csv files that have been provided by WGU. The algorithm used to determine 
     the order in which addresses are chosen is the nearest neighbor algorithm 
     which has a big-O time complexity of O(n^2) and the algorithm used to group
     packages together in loads is a modified greedy algorithm with a big-O time
     complexity of O(n^2). The entire program has a big-O time complexity of 
     O(n^3) with a spacial complexity of O(n^2).
     
     
     
     Below many variables are created to represent the constraints and information provided
     in the task requirements. With the given information and requirements, the simulation 
     finishes with a total of 110.1 mi traveled.
    """

    #Creates the package hash table, main graph and tests out truck delivery options
    ALL_PACKAGES = [i for i in range(1, 41)] #The package ids for the given packages
    places, graph = create_graph_and_places() #Adjacency matrix and place names for given WGU file
    packages = read_package_data('clean_packages.csv') #Creates list of package data from given WGU file
    package_hash = ChainHashTable() #Initialize hash table
    insert_all_packages(packages, package_hash) #Add all packages to hash table
    address_graph = Graph(places, graph)#Creates a graph data structure with all nodes



    display_title() #Shows the application title and description

    #Create Trucks
    truck1 = Truck(1, time(8, 0, 0))
    truck2 = Truck(2, time(9, 5, 0)) #Will leave at 9:05 to deliver the delayed packages
    trucks = [truck1, truck2]

    #Prompt user input for package ids to check along with time
    package_ids, to_time = get_inputs(trucks)
    if not package_ids:
        package_ids = ALL_PACKAGES

    #Creates the loads based on package constraints
    packages_needed = [
        [13, 14, 15, 16, 19, 20, 29, 31, 40], #packages that must be together or have other time constraints
        [25, 3, 6, 18, 28, 32, 36, 38],# packages that are delayed until 9:05 or must be in Truck 2
        [9] #Package 9 must be loaded after 10:20
    ]

    loads = create_all_loads(3, ALL_PACKAGES.copy(), packages_needed, package_hash)


    #Delivers the first 2 loads
    truck1.load_and_deliver(loads[0], package_hash, address_graph)
    truck2.load_and_deliver(loads[1], package_hash, address_graph)
    #Truck 1 waits until 10:20 and package 9 is updated
    truck1.time = time(10, 20, 0) #Waits until 10:20 at the hub
    package9 = package_hash.search(9)
    package9.address = '410 S State St' #Updated address
    #Delivers the last load
    truck1.load_and_deliver(loads[2], package_hash, address_graph)

    #Display progress for each truck
    truck1.display()
    truck2.display()

    #Confirm the time of the status update
    if not to_time: #if no user input for time, display time that truck 1 finished delivery
        to_time = truck1.time

    #Display package statuses and total miles traveled
    print('================================================================')
    print('Package Status at', to_time)
    print('================================================================')
    package_hash.display(package_ids)
    print("================================================================")
    print("\t\tTotal Distance Traveled:", round(truck1.mi_traveled + truck2.mi_traveled, 2), 'mi')



