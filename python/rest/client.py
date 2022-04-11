import json

import numpy as np
import requests

_EXP_DTYPE = np.dtype("float64")
"""The expected dtype for the numpy arrays."""


class DemoRESTClient:
    """This class acts as a client to the service provided by the API REST server
    of this same project. It has several public methods which allow for direct interaction with
    the server, without having to care about the formatting of the RESTful queries.
    """

    # =================================================================================================
    # PUBLIC METHODS for Client operations
    # =================================================================================================

    def __init__(self, host, port, user=None, pwd=None, client=None):
        """The class initializer method.

        Parameters
        ----------
        host : str
            The host (IP/DNS) where the destination server is located.
        port : int
            The port which is exposed by the destination server.
        user : str, optional
            The username to be used in basic authentication, by default None.
        pwd : str, optional
            The password to be used in basic authentication, by default None
        client : FlaskClient
            The Flask client (to be used only for testing purposes).
        """
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd

        # Depending if we are testing or not... it may be needed to pass the
        # FlaskClient directly...
        if client is not None:
            self._use_test_client = True
            self._client = client
        else:
            self._use_test_client = False

    def get_connection_details(self):
        """Get a simple summary of the connection details."""

        # Check that we are not using a test client
        if self._use_test_client:
            print("Using a test client. Unnecessary info.")
            return

        # First, print the basic details of the connection
        print(
            "Connection to host "
            + self._host
            + " through port "
            + str(self._port)
            + " for using the demo-eigen-wrapper package as a REST Service."
        )

        # Add, as well, credential details if available
        if self._user is not None:
            print(">>> User: " + self._user)

        if self._pwd is not None:
            print(">>> Pwd: " + self._pwd)

    def add(self, arg1, arg2):
        """Perform the "add" operation of two numpy.ndarrays using the Eigen library
        (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            The first numpy.ndarray to be considered in the operation.
        arg2 : numpy.ndarray
            The second numpy.ndarray to be considered in the operation.

        Returns
        -------
        numpy.ndarray
            The result of the addition of arg1 and arg2 (i.e. arg1 + arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # Perform the server-related operations
        return self.__perform_operation(arg1, arg2, arg_dim, "add")

    def subtract(self, arg1, arg2):
        """Perform the "subtract" operation of two numpy.ndarrays using the Eigen library
        (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            The first numpy.ndarray to be considered in the operation.
        arg2 : numpy.ndarray
            The second numpy.ndarray to be considered in the operation.

        Returns
        -------
        numpy.ndarray
            The result of the subtraction of arg1 and arg2 (i.e. arg1 - arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # This operation is not even required to be implemented in the server side...
        # Just negate arg2... and perform the server-related operations. Pretty easy!
        return self.__perform_operation(arg1, np.negative(arg2), arg_dim, "add")

    def multiply(self, arg1, arg2):
        """Perform the "multiplication" operation of two numpy.ndarrays using the Eigen library
        (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            The first numpy.ndarray to be considered in the operation.
        arg2 : numpy.ndarray
            The second numpy.ndarray to be considered in the operation.

        Returns
        -------
        numpy.ndarray
            The result of the multiplication of arg1 and arg2 (i.e. arg1 * arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # Perform the server-related operations
        return self.__perform_operation(arg1, arg2, arg_dim, "multiply")

    # =================================================================================================
    # PRIVATE METHODS for Client operations
    # =================================================================================================

    def __check_args(self, arg1, arg2):
        """Sanity-checks private method to ensure that the provided arguments respect
        the expected inputs by the server (to avoid destination server error-throw, whenever possible).

        Parameters
        ----------
        arg1 : numpy.ndarray
            The first numpy.ndarray to be considered in the operation.
        arg2 : numpy.ndarray
            The second numpy.ndarray to be considered in the operation.

        Returns
        -------
        int
            The shape of the involved numpy.ndarrays.

        Raises
        ------
        RuntimeError
            If the first argument (arg1) is not a numpy.ndarray of type numpy.float64.
        RuntimeError
            If the second argument (arg1) is not a numpy.ndarray of type numpy.float64.
        RuntimeError
            If the arguments have different shapes.
        RuntimeError
            If the dimensions of the arguments are not handled by the destination server.
        """
        # Ensure that both arg1 and arg2 are np.ndarrays
        if (isinstance(arg1, np.ndarray) is not True) or (arg1.dtype is not _EXP_DTYPE):
            raise RuntimeError(
                "First argument is not a numpy.ndarray of dtype numpy.float64. Check inputs."
            )
        if (isinstance(arg2, np.ndarray) is not True) or (arg2.dtype is not _EXP_DTYPE):
            raise RuntimeError(
                "Second argument is not a numpy.ndarray of dtype numpy.float64. Check inputs."
            )

        # Check as well that both numpy.ndarrays are of the same shape
        if arg1.shape == arg2.shape:
            arg_dim = len(arg1.shape)
        else:
            raise RuntimeError("Arguments have different shapes. Check inputs.")

        # Return the dimension of the arguments (if it is of the handled types)
        if arg_dim in (1, 2):
            return arg_dim
        else:
            raise RuntimeError(
                "Only numpy.ndarrays of 1D (i.e. vectors) or 2D (i.e. matrices) are allowed. Check inputs."
            )

    def __perform_operation(self, arg1, arg2, arg_dim, ops):
        """Generalistic private method to handle operations with resources Vectors and Matrices of
        the destination server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            The first numpy.ndarray to be considered in the operation.
        arg2 : numpy.ndarray
            The second numpy.ndarray to be considered in the operation.
        arg_dim : int
            The shape of the involved numpy.ndarrays.
        ops : str
            The type of operation to be carried out (i.e. "add", "multiply").

        Returns
        -------
        numpy.ndarray
            The result of the operation requested between arg1 and arg2.
        """
        # At this point we must check if we are dealing with a vector or a matrix...
        # and proceed to perform the requested operation
        if arg_dim == 1:
            id1 = self.__post_resource(arg1, "Vectors")
            id2 = self.__post_resource(arg2, "Vectors")
            return self.__get_ops_resource(id1, id2, ops, "Vectors")
        else:
            id1 = self.__post_resource(arg1, "Matrices")
            id2 = self.__post_resource(arg2, "Matrices")
            return self.__get_ops_resource(id1, id2, ops, "Matrices")

    def __post_resource(self, arg, resource):
        """Generalistic private method to handle the posting of objects to the destination server.

        Parameters
        ----------
        arg : numpy.ndarray
            The numpy.ndarray to be posted to the destination server.
        resource : str
            The type of resource where the posting will be performed.

        Returns
        -------
        int
            The ID of the posted object.

        Raises
        ------
        RuntimeError
            If the Client failed to connect to the destination server.
        RuntimeError
            If the Client failed to post the argument to the destination server.
        """
        # Perform the post request
        try:
            if not self._use_test_client:
                response = requests.post(
                    self._host + ":" + str(self._port) + "/" + resource,
                    json={"value": arg.tolist()},
                    auth=(self._user, self._pwd),
                )
            else:
                response = self._client.post(
                    "/" + resource,
                    json={"value": arg.tolist()},
                    auth=(self._user, self._pwd),
                )
        except (requests.exceptions.ConnectionError):
            raise RuntimeError(
                "Could not connect to server... Check server status or connection details."
            )

        # Check that the status of the response is correct
        if response.status_code != 201:
            raise RuntimeError("Client failed to post object in destination Server...")

        # If everything went well... extract the id of the posted object
        return self.__get_val(json.loads(response.text), "id")

    def __get_ops_resource(self, id1, id2, ops, resource):
        """_summary_

        Parameters
        ----------
        id1 : int
            The ID (in the destination server) of the first argument involved in the operation.
        id2 : int
            The ID (in the destination server) of the second argument involved in the operation.
        ops : str
            The type of operation to be performed.
        resource : str
            The type of resource involved in the requested operation.

        Returns
        -------
        numpy.ndarray
            The result of the operation requested.

        Raises
        ------
        RuntimeError
            If the Client failed to connect to the destination server.
        RuntimeError
            If the Client failed to perform the operation in the destination server.
        """
        # Perform the get request
        try:
            if not self._use_test_client:
                response = requests.get(
                    self._host + ":" + str(self._port) + "/" + ops + "/" + resource,
                    json={"id1": id1, "id2": id2},
                    auth=(self._user, self._pwd),
                )
            else:
                response = self._client.get(
                    "/" + ops + "/" + resource,
                    json={"id1": id1, "id2": id2},
                    auth=(self._user, self._pwd),
                )
        except (requests.exceptions.ConnectionError):
            raise RuntimeError(
                "Could not connect to server... Check server status or connection details."
            )

        # Check that the status of the response is correct
        if response.status_code != 200:
            raise RuntimeError(
                "Client failed to perform operation in destination Server..."
            )

        # If everything went well... extract the result of the operation
        result_aslist = json.loads(self.__get_val(json.loads(response.text), "result"))

        # From the JSON response, when parsed, the result will be considered as a simple
        # Python object (double, list of doubles...). Convert it to a numpy.ndarray object
        return np.array(result_aslist, dtype=np.float64)

    def __get_val(self, search_dict, key):
        """Private method to iterate recursively inside a multidict.

        This method has been gratefully used from https://stackoverflow.com/a/66668504

        Parameters
        ----------
        search_dict : dict
            The dict/multidict we want to search in.
        key : str
            The key we are interested in looking for.

        Returns
        -------
        Any
            The value we are interested in.
        """
        for elem in search_dict:
            if elem == key:
                return search_dict[elem]
            if isinstance(search_dict[elem], dict):
                retval = self.__get_val(search_dict[elem], key)
                if retval is not None:
                    return retval
