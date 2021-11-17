class Package:
    """
    This class represents a package.

    Attributes
    ----------
    id : int
        The unique ID of the package
    address : str
        The address of the package's destination
    deadline : str
        The time that the package must be delivered by
    city : str
        The city of the package's destination
    zipcode : str
        The zipcode of the package's destination
    weight : str
        The weight of the package
    status : str
        The status of whether the package has been delivered, is en route, or at the hub
         (default is "at the hub")
    time_left : datetime.time
        The time the package left its hub (default = None)
    """
    #O(1)
    def __init__(self, id, address, deadline, city, zipcode, weight,
                 status="at the hub", time_left=None):
        """
        Parameters
        ----------
        id : str
            The unique ID of the package
        address : str
            The address of the package's destination
        deadline : str
            The time that the package must be delivered by
        city : str
            The city of the package's destination
        zipcode : str
            The zipcode of the package's destination
        weight : str
            The weight of the package
        status : bool
            The status of whether the package has been delivered (default is False)
        time_left : datetime.time
            The time the package left its hub (default = None)
        """
        self.id = int(id)
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = int(weight)
        self.status = status
        self.time_left = time_left
