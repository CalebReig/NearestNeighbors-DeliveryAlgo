"""
read_data

This python file contains functions to read csv files and parse its data.
There are functions to perform these tasks on two different types of csv files.
One file needs to be a fully filled adjacency matrix with place names as the header.
This type of file will be read and parsed with the following functions:

        * read_adjacency_matrix - parses place names and distances from a csv file
        * clean_places - removes unnecessary spaces and words from the parsed places
        * clean_matrix - transforms the distances from strings to float
        * create_graph_and_places - using the above functions, reads in a csv file and parses its data

The other file needs to be a csv file containing package data with id, address, city, state,
zip code, delivery deadline, weight and special notes. This type of file will be read and parsed
with the following function:

        * read_package_data - reads a csv file and returns a list of packages

"""

import csv

#=======================================================================
#Functions for reading in adjacency matrix data


# O(n)
def read_adjacency_matrix(csv_file):
    """
    This function parses place names and distances from an adjacency matrix csv file.

    The file must be formatted with place names as the header and the adjacency matrix fully filled.

    Parameters
    ----------
    csv_file : str
        A csv file in the form of an adjacency matrix with place names as header

    Returns
    ----------
    list[str]
        A list of places that are the nodes of the adjacency matrix.

    list[list[str]]
        A 2D list representing the distance between nodes
    """
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        places = []
        graph = []
        for i, row in enumerate(reader):
            if i == 0:
                places = row
            else:
                graph.append(row)
        return places, graph


# O(n)
def clean_places(places):
    """
    This function removes unnecessary spaces and words from a list of places.

    Parameters
    ----------
    places : list[str]
        A list of place names that have not been cleaned

    Returns
    ----------
    list[str]
        A list of places that are the nodes of the adjacency matrix.
    """
    new_places = []
    for i, place in enumerate(places):
        split = place.split('\n')
        if i == 0:
            new_place = split[1].strip(', ')
        else:
            new_place = (' '.join(split[1:])).strip()
        new_places.append(new_place)
    return new_places

# O(n^2)
def clean_matrix(matrix):
    """
    Transforms a matrix of type string to type float

    Parameters
    ----------
    matrix : list[list[str]]
        An adjacency matrix with elements of type string

    Returns
    ----------

    list[list[float]]
        A 2D list representing the distance between nodes
    """
    new_matrix = [[None for i in range(len(matrix))] for i in range(len(matrix))]
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            new_item = float(item)
            new_matrix[i][j] = new_item

    return new_matrix

#O(n^2)
def create_graph_and_places():
    """
    Parses place names and an adjacency matrix from the 'adjacencyMtrx.csv' file.

    Returns
    ----------
    list[str]
        A list of places that are the nodes of the adjacency matrix.

    list[list[float]]
        A 2D list representing the distance between nodes
    """
    places, graph = read_adjacency_matrix('adjacencyMtrx.csv')  #O(n)
    places = clean_places(places)                               #O(n)
    graph = clean_matrix(graph)                                 #O(n^2)
    return places, graph

#=======================================================================
#Function for reading in package data

#O(n)
def read_package_data(csv_file):
    """
    Parses package data out of a csv file.

    Parameters
    ----------
    csv_file : str
        The name of the csv file to be parsed

    Returns
    ----------

    list[str]
        A list of comma separated values describing individual packages
    """
    with open(csv_file, 'r') as f:
        packages = []
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(reader):
            if i != 0:
                packages.append(row)
    return packages
