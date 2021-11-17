class Graph:
    """
    This class represent a fully connected weighted graph.

    Attributes
    ----------
    places : list[str]
        a list of places that are the nodes of the graph
    matrix : list[list[float]]
        an adjacency matrix to represent distances of nodes

    Methods
    -------
    create_partial_graph(sub_places)
        Creates a new graph that is a subset of the current graph

    find_nearest_neighbor(start)
        finds the closest node to the given node
    """

    #O(1)
    def __init__(self, places, matrix):
        """
        Parameters
        ----------
        places : list[str]
            a list of places that are the nodes of the graph
        matrix : list[list[float]]
            an adjacency matrix to represent distances of nodes
        """
        self.places = places
        self.matrix = matrix

    #O((n * (n-1))/2) = O(n^2)
    #Where n = number of nodes in current graph
    def create_partial_graph(self, sub_places, inplace=False):
        """
        Creates a subgraph of the current graph based on a subset of place names.

        Parameters
        ----------
        sub_places : list[str]
            a subset of places

        inplace : bool
            if True, will alter the current graph's matrix (default = False)

        Returns
        ----------
        2D list
            a new adjacency matrix with the same or fewer nodes
        """
        indexes = []
        for place in sub_places:
            indexes.append(self.places.index(place))
        indexes.sort()
        new_matrix = []
        for i, row in enumerate(self.matrix):
            if i in indexes:
                new_row = []
                for ix in indexes:
                    new_row.append(row[ix])
                new_matrix.append(new_row)
        if inplace:
            self.matrix = new_matrix
            self.places = sub_places
        return new_matrix

    #O(n)
    def find_nearest_neighbor(self, start):
        """
        Finds the nearest node of a given node.

        Parameters
        ----------
        start : str
            The name of the starting node to reference

        Returns
        ----------
        str
            The place name of the nearest node
        float
            The distance between the nodes
        """
        start_ix = self.places.index(start)
        min = 100
        ix = None
        for i, dist in enumerate(self.matrix[start_ix]):
            if dist < min and dist != 0:
                min = dist
                ix = i
        return self.places[ix], min