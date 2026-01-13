# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Python implementation of the REST API Eigen example client."""

import json

import numpy as np
import requests

_EXP_DTYPE = np.dtype("float64")
"""Expected dtype for numpy arrays."""


class DemoRESTClient:
    """Acts as a client to the service provided by the API REST server of this same project.
    This class has several public methods that allow for direct interaction with the server,
    without having to care about the formatting of the RESTful queries.
    """

    # =================================================================================================
    # PUBLIC METHODS for Client operations
    # =================================================================================================

    def __init__(self, host, port, user=None, pwd=None, client=None):
        """Initialize the client.

        Parameters
        ----------
        host : str
            Host (IP/DNS) where the destination server is located.
        port : int
            Port that is exposed by the destination server.
        user : str, optional
            Username to use in basic authentication. The default is ``None``.
        pwd : str, optional
            Password to use in basic authentication. The default is ``None``.
        client : FlaskClient
            Flask client, which is to be used only for testing purposes. The default is ``None``.
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
        """Add two numpy.ndarrays using the Eigen library (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            First numpy.ndarray to consider in the operation.
        arg2 : numpy.ndarray
            Second numpy.ndarray to consider in the operation.

        Returns
        -------
        numpy.ndarray
            Sum of adding arg1 and arg2 (arg1 + arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # Perform the server-related operations
        return self.__perform_operation(arg1, arg2, arg_dim, "add")

    def subtract(self, arg1, arg2):
        """Subtract two numpy.ndarrays using the Eigen library
        (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            First numpy.ndarray to consider in the operation.
        arg2 : numpy.ndarray
            Second numpy.ndarray to consider in the operation.

        Returns
        -------
        numpy.ndarray
            The result of subtracting arg2 from arg1 (arg1 - arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # This operation is not even required to be implemented in the server side...
        # Just negate arg2... and perform the server-related operations. Pretty easy!
        return self.__perform_operation(arg1, np.negative(arg2), arg_dim, "add")

    def multiply(self, arg1, arg2):
        """Multiply two numpy.ndarrays using the Eigen library (C++), which is exposed via the destination RESTful server.

        Parameters
        ----------
        arg1 : numpy.ndarray
            First numpy.ndarray to consider in the operation.
        arg2 : numpy.ndarray
            Second numpy.ndarray to consider in the operation.

        Returns
        -------
        numpy.ndarray
            The result of multiplyng arg1 and arg2 (arg1 * arg2).
        """
        # Check that the provided arguments are inline with the handled parameters by our service
        arg_dim = self.__check_args(arg1, arg2)

        # Perform the server-related operations
        return self.__perform_operation(arg1, arg2, arg_dim, "multiply")

    # =================================================================================================
    # PRIVATE METHODS for Client operations
    # =================================================================================================

    def __check_args(self, arg1, arg2):
        """Check that provided arguments respect the expected inputs by the server. The goal of this
        private method is to avoid destination server error-throw whenever possible.

        Parameters
        ----------
        arg1 : numpy.ndarray
            First numpy.ndarray to consider in the operation.
        arg2 : numpy.ndarray
            Second numpy.ndarray to consider in the operation.

        Returns
        -------
        int
            Shape of the involved numpy.ndarrays.

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
            First numpy.ndarray to consider in the operation.
        arg2 : numpy.ndarray
            Second numpy.ndarray to consider in the operation.
        arg_dim : int
            Shape of the involved numpy.ndarrays.
        ops : str
            Type of operation to carry out. For example, "add" or "multiply".

        Returns
        -------
        numpy.ndarray
            Tesult of the operation requested between arg1 and arg2.
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
            The numpy.ndarray to post to the destination server.
        resource : str
            Type of resource where the posting is to be performed.

        Returns
        -------
        int
            ID of the posted object.

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
            ID (in the destination server) of the first argument in the operation.
        id2 : int
            ID (in the destination server) of the second argument in the operation.
        ops : str
            Type of operation to perform.
        resource : str
            Type of resource involved in the operation.

        Returns
        -------
        numpy.ndarray
            Result of the operation requested.

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
        result_aslist = self.__get_val(json.loads(response.text), "result")

        # From the JSON response, when parsed, the result will be considered as a simple
        # Python object (double, list of doubles...). Convert it to a numpy.ndarray object
        return np.array(result_aslist, dtype=np.float64)

    def __get_val(self, search_dict, key):
        """Private method to iterate recursively inside a multidict.

        This method has been gratefully used from https://stackoverflow.com/a/66668504

        Parameters
        ----------
        search_dict : dict
            Dictionary or multiple dictionaries to search.
        key : str
            Key to search for.

        Returns
        -------
        Any
            Value of interest.
        """
        for elem in search_dict:
            if elem == key:
                return search_dict[elem]
            if isinstance(search_dict[elem], dict):
                retval = self.__get_val(search_dict[elem], key)
                if retval is not None:
                    return retval
