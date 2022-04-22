"""The Python implementation of the gRPC API Eigen example client."""

import time

import grpc
import numpy as np

import ansys.grpc.constants as constants
import ansys.grpc.generated.grpcdemo_pb2 as grpcdemo_pb2
import ansys.grpc.generated.grpcdemo_pb2_grpc as grpcdemo_pb2_grpc


class DemoGRPCClient:
    """The API Eigen Example client class for interacting via gRPC."""

    def __init__(self, ip="127.0.0.1", port=50051, timeout=1, test=None):
        """Initialize connection to the API Eigen server.

        Parameters
        ----------
        ip : str, optional
            The IP or DNS to which we want to connect, by default "127.0.0.1".
        port : int, optional
            The port which we want to connect to, by default 50051.
        timeout : int, optional
            The number of seconds we will wait before returning a timeout in the connection, by default 1.
        test : object, optional
            The test GRPCDemoStub we will connect to in case provided, by default None. This argument is only intended for test puposes.

        Raises
        ------
        IOError
            In case our client was unable to connect to the server.
        """
        # For test purposes, provide a stub directly
        if test is not None:
            self._stub = test
            return

        self._stub = None
        self._channel_str = "%s:%d" % (ip, port)

        self.channel = grpc.insecure_channel(self._channel_str)
        self._state = grpc.channel_ready_future(self.channel)
        self._stub = grpcdemo_pb2_grpc.GRPCDemoStub(self.channel)

        # Verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:
            raise IOError("Unable to connect to server at %s" % self._channel_str)
        else:
            print("Connected to server at %s:%d" % (ip, port))

    # =================================================================================================
    # PUBLIC METHODS for Client operations
    # =================================================================================================

    def request_greeting(self, name):
        """Method which requests a greeting from the server.

        Parameters
        ----------
        name : str
            The name of the "client" (e.g. "Michael").
        """
        # Build the greeting request
        request = grpcdemo_pb2.HelloRequest(name=name)

        # Send the request
        response = self._stub.SayHello(request)

        # Show the server's response
        print("The server answered: " + response.message)

    def flip_vector(self, vector):
        """Method to flip a numpy.ndarray vector psoitions, such that [A, B, C, D] --> [D, C, B, A].

        Parameters
        ----------
        vector : numpy.ndarray
            The vector we want to flip.

        Returns
        -------
        numpy.ndarray
            The flipped vector.
        """
        # Build the stream (i.e. generator)
        vector_gen = self._generate_vector_stream(vector)

        # Retrieve only the first element - vector is a single numpy.ndarray (or should be!)
        request = next(vector_gen)

        # Call the server method and retrieve the result
        vec_flip = self._stub.FlipVector(request)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(vec_flip)

        return nparray

    def add_vectors(self, *args):
        """Method to add numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The result of the addition of the given numpy.ndarrays.
        """
        # Build the stream (i.e. generator)
        vector_iterator = self._generate_vector_stream(*args)

        # Call the server method and retrieve the result
        vector_addition = self._stub.AddVectors(vector_iterator)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(vector_addition)

        return nparray

    def multiply_vectors(self, *args):
        """Method to perform dot product of numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The result of the dot product. Despite returning a numpy.ndarray, it will only contain one value since it is a dot product.
        """
        # Build the stream (i.e. generator)
        vector_iterator = self._generate_vector_stream(*args)

        # Call the server method and retrieve the result
        vector_mult = self._stub.MultiplyVectors(vector_iterator)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(vector_mult)

        return nparray

    def add_matrices(self, *args):
        """Method to add numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The resulting numpy.ndarray of the matrices addition.
        """
        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(*args)

        # Call the server method and retrieve the result
        matrix_addition = self._stub.AddMatrices(matrix_iterator)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(matrix_addition)

        return nparray

    def multiply_matrices(self, *args):
        """Method to perform the product of numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The resulting numpy.ndarray of the matrices multiplication.
        """
        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(*args)

        # Call the server method and retrieve the result
        matrix_mult = self._stub.MultiplyMatrices(matrix_iterator)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(matrix_mult)

        return nparray

    # =================================================================================================
    # PRIVATE METHODS for Client operations
    # =================================================================================================

    def _generate_vector_stream(self, *args):
        # Loop over all input arguments
        for arg in args:
            # Perform some argument input sanity checks
            if type(arg) is not np.ndarray:
                raise RuntimeError("Invalid argument. Only numpy.ndarrays allowed.")
            elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
                raise RuntimeError(
                    "Invalid argument. Only numpy.ndarrays of type int32 and float64 allowed."
                )
            elif arg.ndim != 1:
                raise RuntimeError("Invalid argument. Only 1D numpy.ndarrays allowed.")

            # If sanity checks went fine... yield the corresponding Vector message
            yield grpcdemo_pb2.Vector(
                data_type=constants.NP_DTYPE_TO_DATATYPE[arg.dtype.type],
                vector_size=arg.shape[0],
                vector_as_chunk=arg.tobytes(),
            )

    def _read_nparray_from_vector(self, vector):
        # Convert Vector message to a numpy.ndarray to continue nominal operations (outside the client)
        dtype = None
        if vector.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
            dtype = np.int32
        elif vector.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
            dtype = np.float64

        return np.frombuffer(vector.vector_as_chunk, dtype=dtype)

    def _generate_matrix_stream(self, *args):
        # Loop over all input arguments
        for arg in args:
            # Perform some argument input sanity checks
            if type(arg) is not np.ndarray:
                raise RuntimeError("Invalid argument. Only numpy.ndarrays allowed.")
            elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
                raise RuntimeError(
                    "Invalid argument. Only numpy.ndarrays of type int32 and float64 allowed."
                )
            elif arg.ndim != 2:
                raise RuntimeError("Invalid argument. Only 2D numpy.ndarrays allowed.")

            # If sanity checks went fine... yield the corresponding Matrix message
            yield grpcdemo_pb2.Matrix(
                data_type=constants.NP_DTYPE_TO_DATATYPE[arg.dtype.type],
                matrix_rows=arg.shape[0],
                matrix_cols=arg.shape[1],
                matrix_as_chunk=arg.tobytes(),
            )

    def _read_nparray_from_matrix(self, matrix):
        # Convert Matrix message to a numpy.ndarray to continue nominal operations (outside the client)
        dtype = None
        if matrix.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
            dtype = np.int32
        elif matrix.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
            dtype = np.float64

        # Load into a 1D numpy array....
        nparray = np.frombuffer(matrix.matrix_as_chunk, dtype=dtype)

        # ... and reshape it according to the Matrix message vefore returning it
        return np.reshape(
            nparray,
            (
                matrix.matrix_rows,
                matrix.matrix_cols,
            ),
        )
