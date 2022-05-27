"""The Python implementation of the gRPC API Eigen example client."""

import time

import grpc
import numpy as np

import ansys.eigen.python.grpc.constants as constants
import ansys.eigen.python.grpc.generated.grpcdemo_pb2 as grpcdemo_pb2
import ansys.eigen.python.grpc.generated.grpcdemo_pb2_grpc as grpcdemo_pb2_grpc


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
        # Generate the metadata and the amount of chunks per Vector
        md, chunks = self._generate_md("vectors", "vec", vector)

        # Build the stream (i.e. generator)
        vector_gen = self._generate_vector_stream(chunks, vector)

        # Call the server method and retrieve the result
        response_iterator = self._stub.FlipVector(vector_gen, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (we are expecting a single vector)
        return nparray[0]

    def add_vectors(self, *args):
        """Method to add numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The result of the addition of the given numpy.ndarrays.
        """
        # Generate the metadata and the amount of chunks per Vector
        md, chunks = self._generate_md("vectors", "vec", *args)

        # Build the stream (i.e. generator)
        vector_iterator = self._generate_vector_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.AddVectors(vector_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (we are expecting a single vector)
        return nparray[0]

    def multiply_vectors(self, *args):
        """Method to perform dot product of numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The result of the dot product. Despite returning a numpy.ndarray, it will only contain one value since it is a dot product.
        """
        # Generate the metadata and the amount of chunks per Vector
        md, chunks = self._generate_md("vectors", "vec", *args)

        # Build the stream (i.e. generator)
        vector_iterator = self._generate_vector_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.MultiplyVectors(vector_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (we are expecting a single vector)
        return nparray[0]

    def add_matrices(self, *args):
        """Method to add numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The resulting numpy.ndarray of the matrices addition.
        """
        # Generate the metadata and the amount of chunks per Matrix
        md, chunks = self._generate_md("matrices", "mat", *args)

        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.AddMatrices(matrix_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(response_iterator)

        # Return only the first element (we are expecting a single matrix)
        return nparray[0]

    def multiply_matrices(self, *args):
        """Method to perform the product of numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            The resulting numpy.ndarray of the matrices multiplication.
        """
        # Generate the metadata and the amount of chunks per Matrix
        md, chunks = self._generate_md("matrices", "mat", *args)

        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.MultiplyMatrices(matrix_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(response_iterator)

        # Return only the first element (we are expecting a single matrix)
        return nparray[0]

    # =================================================================================================
    # PRIVATE METHODS for Client operations
    # =================================================================================================

    def _generate_md(self, message_type: str, abbrev: str, *args: np.ndarray):
        # Initialize the metadata and the chunks list for each full message
        md = []
        chunks = []

        # Find how many arguments we are transmitting
        md.append(("full-" + message_type, str(len(args))))

        # Loop over all input arguments
        idx = 1
        for arg in args:
            # Perform some argument input sanity checks
            if message_type == "vectors" and abbrev == "vec":
                self._sanity_check_vector(arg)
            elif message_type == "matrices" and abbrev == "mat":
                self._sanity_check_matrix(arg)
            else:
                raise RuntimeError("Invalid usage of _generate_md function.")

            # Check the size of the arrays
            # If size is surpassed, determine chunks needed
            if arg.nbytes > constants.MAX_CHUNKSIZE:
                # Let us determine how many chunks we will need
                #
                # Max amount of elements per chunk
                max_elems = constants.MAX_CHUNKSIZE // arg.itemsize

                # Bulk number of chunks needed
                bulk_chunks = arg.size // max_elems

                # The remainder amount of elements (if any)
                remainder = arg.size % max_elems

                # This list will preovide us with the last index up to which to
                # process in each partial Vector/Matrix message
                last_idx_chunk = []
                for i in range(1, bulk_chunks + 1):
                    last_idx_chunk.append(i * max_elems)

                # Take into account that if there is a remainder, we should
                # include one last partial Vector/Matrix message.
                if remainder != 0:
                    last_idx_chunk.append(arg.size)

                # Finally append the results
                md.append((abbrev + str(idx) + "-messages", str(len(last_idx_chunk))))
                chunks.append(last_idx_chunk)

            else:
                # Otherwise we are dealing with a single message.. Append results!
                md.append((abbrev + str(idx) + "-messages", str(1)))
                chunks.append([arg.size])

            # Increase idx by 1
            idx += 1

        # Return the metadata and the chunks list for each Vector/Matrix
        return md, chunks

    def _generate_vector_stream(self, chunks: "list[list[int]]", *args: np.ndarray):
        # Loop over all input arguments
        for arg, vector_chunks in zip(args, chunks):
            # Perform some argument input sanity checks
            self._sanity_check_vector(arg)

            # If sanity checks went fine... yield the corresponding Vector message
            #
            # Loop over the chunk indices
            processed_idx = 0
            for last_idx_chunk in vector_chunks:
                # Use tmp_idx in yield function and update the processed_idx afterwards
                tmp_idx = processed_idx
                processed_idx = last_idx_chunk

                # Yield!
                yield grpcdemo_pb2.Vector(
                    data_type=constants.NP_DTYPE_TO_DATATYPE[arg.dtype.type],
                    vector_size=arg.shape[0],
                    vector_as_chunk=arg[tmp_idx:last_idx_chunk].tobytes(),
                )

    def _generate_matrix_stream(self, chunks: "list[list[int]]", *args: np.ndarray):
        # Loop over all input arguments
        for arg, matrix_chunks in zip(args, chunks):
            # Perform some argument input sanity checks
            self._sanity_check_matrix(arg)

            # If sanity checks went fine... yield the corresponding Matrix message
            #
            # Since we are dealing with matrices, ravel it to a 1D array (avoids copy)
            arg_as_vec = arg.ravel()

            # Loop over the chunk indices
            processed_idx = 0
            for last_idx_chunk in matrix_chunks:
                # Use tmp_idx in yield function and update the processed_idx afterwards
                tmp_idx = processed_idx
                processed_idx = last_idx_chunk

                # Yield!
                yield grpcdemo_pb2.Matrix(
                    data_type=constants.NP_DTYPE_TO_DATATYPE[arg.dtype.type],
                    matrix_rows=arg.shape[0],
                    matrix_cols=arg.shape[1],
                    matrix_as_chunk=arg_as_vec[tmp_idx:last_idx_chunk].tobytes(),
                )

    def _read_nparray_from_vector(self, response_iterator):
        # First, get the metadata
        response_md = response_iterator.initial_metadata()

        # Parse the server's metadata
        full_msg, chunks_per_msg = self._parse_server_metadata(response_md)

        # Initialize the output list
        resulting_vectors = []

        # Let us start processing messages independently
        for msg in range(full_msg):
            # Init the resulting numpy.ndarray to None, its size and its type
            result = None
            result_size = 0
            result_dtype = None

            # Loop over the available chunks per message
            for chunk_idx in range(chunks_per_msg[msg]):
                # Read a message
                vector = next(response_iterator)

                # If it is the first chunk we are processing, parse dtype and size
                if chunk_idx == 0:
                    if vector.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
                        result_dtype = np.int32
                    elif vector.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
                        result_dtype = np.float64

                    result_size = vector.vector_size

                # Parse the chunk
                if result is None:
                    result = np.frombuffer(vector.vector_as_chunk, dtype=result_dtype)
                else:
                    tmp = np.frombuffer(vector.vector_as_chunk, dtype=result_dtype)
                    result = np.concatenate((result, tmp))

            # Check if the final Vector has the desired size
            if result.size != result_size:
                raise RuntimeError("Problems reading server full Vector message...")
            else:
                # If everything went fine, append to resulting_vectors list
                resulting_vectors.append(result)

        # Return the resulting_vectors list
        return resulting_vectors

    def _read_nparray_from_matrix(self, response_iterator):
        # First, get the metadata
        response_md = response_iterator.initial_metadata()

        # Parse the server's metadata
        full_msg, chunks_per_msg = self._parse_server_metadata(response_md)

        # Initialize the output list
        resulting_matrices = []

        # Let us start processing messages independently
        for msg in range(full_msg):
            # Init the resulting numpy.ndarray to None, its size (rows,cols) and its type
            result = None
            result_rows = 0
            result_cols = 0
            result_dtype = None

            # Loop over the available chunks per message
            for chunk_idx in range(chunks_per_msg[msg]):
                # Read a message
                matrix = next(response_iterator)

                # If it is the first chunk we are processing, parse dtype and size (rows,cols)
                if chunk_idx == 0:
                    if matrix.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
                        result_dtype = np.int32
                    elif matrix.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
                        result_dtype = np.float64

                    result_rows = matrix.matrix_rows
                    result_cols = matrix.matrix_cols

                # Parse the chunk
                if result is None:
                    result = np.frombuffer(matrix.matrix_as_chunk, dtype=result_dtype)
                else:
                    tmp = np.frombuffer(matrix.matrix_as_chunk, dtype=result_dtype)
                    result = np.concatenate((result, tmp))

            # Check if the final Matrix has the desired size
            if result.size != result_rows * result_cols:
                raise RuntimeError("Problems reading server full Matrix message...")
            else:
                # If everything went fine, append to resulting_matrices list
                resulting_matrices.append(
                    np.reshape(
                        result,
                        (
                            result_rows,
                            result_cols,
                        ),
                    )
                )

        # Return the resulting_matrices list
        return resulting_matrices

    def _sanity_check_vector(self, arg):
        # Perform some argument input sanity checks
        if type(arg) is not np.ndarray:
            raise RuntimeError("Invalid argument. Only numpy.ndarrays allowed.")
        elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
            raise RuntimeError(
                "Invalid argument. Only numpy.ndarrays of type int32 and float64 allowed."
            )
        elif arg.ndim != 1:
            raise RuntimeError("Invalid argument. Only 1D numpy.ndarrays allowed.")

    def _sanity_check_matrix(self, arg):
        # Perform some argument input sanity checks
        if type(arg) is not np.ndarray:
            raise RuntimeError("Invalid argument. Only numpy.ndarrays allowed.")
        elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
            raise RuntimeError(
                "Invalid argument. Only numpy.ndarrays of type int32 and float64 allowed."
            )
        elif arg.ndim != 2:
            raise RuntimeError("Invalid argument. Only 2D numpy.ndarrays allowed.")

    def _parse_server_metadata(self, response_md: "list[tuple]"):
        # Init the return variables: amount of full messages received
        # and partial messages per full message
        full_msg = 0
        chunks_per_msg = []

        # First, find out how many full messages we will be processing
        for md in response_md:
            if md[0] == "full-vectors" or md[0] == "full-matrices":
                full_msg = int(md[1])

        # Now, identify the chunks per message (only if we were successful previously)
        if full_msg != 0:
            for i in range(1, full_msg + 1):
                for md in response_md:
                    if md[0] == "vec%d-messages" % i or md[0] == "mat%d-messages" % i:
                        chunks_per_msg.append(int(md[1]))

        return full_msg, chunks_per_msg
