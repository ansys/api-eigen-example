"""Python implementation of the gRPC API Eigen Example client."""

import grpc
import numpy as np

import ansys.eigen.python.grpc.constants as constants
import ansys.eigen.python.grpc.generated.grpcdemo_pb2 as grpcdemo_pb2
import ansys.eigen.python.grpc.generated.grpcdemo_pb2_grpc as grpcdemo_pb2_grpc


class DemoGRPCClient:
    """Provides the API Eigen Example client class for interacting via gRPC."""

    def __init__(self, ip="127.0.0.1", port=50051, timeout=1, test=None):
        """Initialize connection to the API Eigen server.

        Parameters
        ----------
        ip : str, optional
            IP or DNS to which to connect. The default is "127.0.0.1".
        port : int, optional
            Port to connect to. The default is 50051.
        timeout : int, optional
            Number of seconds to wait before returning a timeout in the connection. The default is 1.
        test : object, optional
            Test GRPCDemoStub to connect to. The default is ``None``. This argument is only intended for test purposes.

        Raises
        ------
        IOError
            Error if the client was unable to connect to the server.
        """
        # For test purposes, provide a stub directly
        if test is not None:
            self._stub = test
            return

        self._stub = None
        self._channel_str = "%s:%d" % (ip, port)

        self.channel = grpc.insecure_channel(self._channel_str)

        # Verify connection
        try:
            grpc.channel_ready_future(self.channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise IOError("Unable to connect to server at %s" % self._channel_str)

        # Set up the stub
        self._stub = grpcdemo_pb2_grpc.GRPCDemoStub(self.channel)

        print("Connected to server at %s:%d" % (ip, port))

    # =================================================================================================
    # PUBLIC METHODS for Client operations
    # =================================================================================================

    def request_greeting(self, name):
        """Method that requests a greeting from the server.

        Parameters
        ----------
        name : str
            Name of the "client". For example, "Michael".
        """
        # Build the greeting request
        request = grpcdemo_pb2.HelloRequest(name=name)

        # Send the request
        response = self._stub.SayHello(request)

        # Show the server's response
        print("The server answered: " + response.message)

    def flip_vector(self, vector):
        """Flip the position of a numpy.ndarray vector such that [A, B, C, D] --> [D, C, B, A].

        Parameters
        ----------
        vector : numpy.ndarray
            Vector to flip.

        Returns
        -------
        numpy.ndarray
            Flipped vector.
        """
        # Generate the metadata and the amount of chunks per vector
        md, chunks = self._generate_md("vectors", "vec", vector)

        # Build the stream (i.e. generator)
        vector_gen = self._generate_vector_stream(chunks, vector)

        # Call the server method and retrieve the result
        response_iterator = self._stub.FlipVector(vector_gen, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (expecting a single vector)
        return nparray[0]

    def add_vectors(self, *args):
        """Add numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            Result of the given numpy.ndarrays.
        """
        # Generate the metadata and the amount of chunks per vector
        md, chunks = self._generate_md("vectors", "vec", *args)

        # Build the stream (i.e. generator)
        vector_iterator = self._generate_vector_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.AddVectors(vector_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (expecting a single vector)
        return nparray[0]

    def multiply_vectors(self, *args):
        """Multiply numpy.ndarray vectors using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            Result of the multiplication of numpy.ndarray vactors. Despite returning a numpy.ndarray, the result only contains one value because it is a dot product.
        """
        # Generate the metadata and the amount of chunks per vector
        md, chunks = self._generate_md("vectors", "vec", *args)

        # Build the stream (generator)
        vector_iterator = self._generate_vector_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.MultiplyVectors(vector_iterator, metadata=md)

        # Convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_vector(response_iterator)

        # Return only the first element (expecting a single vector)
        return nparray[0]

    def add_matrices(self, *args):
        """Add numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            Resulting numpy.ndarray of the matrices addition.
        """
        # Generate the metadata and the amount of chunks per Matrix
        md, chunks = self._generate_md("matrices", "mat", *args)

        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.AddMatrices(matrix_iterator, metadata=md)

        # Now, convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(response_iterator)

        # Return only the first element (expecting a single matrix)
        return nparray[0]

    def multiply_matrices(self, *args):
        """Multiply numpy.ndarray matrices using the Eigen library on the server side.

        Returns
        -------
        numpy.ndarray
            Resulting numpy.ndarray of the matrices' multiplication.
        """
        # Generate the metadata and the amount of chunks per matrix
        md, chunks = self._generate_md("matrices", "mat", *args)

        # Build the stream (i.e. generator)
        matrix_iterator = self._generate_matrix_stream(chunks, *args)

        # Call the server method and retrieve the result
        response_iterator = self._stub.MultiplyMatrices(matrix_iterator, metadata=md)

        # Convert to a numpy.ndarray to continue nominal operations (outside the client)
        nparray = self._read_nparray_from_matrix(response_iterator)

        # Return only the first element (expecting a single matrix)
        return nparray[0]

    # =================================================================================================
    # PRIVATE METHODS for Client operations
    # =================================================================================================

    def _generate_md(self, message_type: str, abbrev: str, *args: np.ndarray):
        # Initialize the metadata and the chunks list for each full message
        md = []
        chunks = []

        # Find how many arguments are transmitting
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
                # Determine how many chunks are needed
                #
                # Max amount of elements per chunk
                max_elems = constants.MAX_CHUNKSIZE // arg.itemsize

                # Bulk number of chunks needed
                bulk_chunks = arg.size // max_elems

                # The remainder amount of elements (if any)
                remainder = arg.size % max_elems

                # This list provides the last index up to which to
                # process in each partial vector or matrix message
                last_idx_chunk = []
                for i in range(1, bulk_chunks + 1):
                    last_idx_chunk.append(i * max_elems)

                # Take into account that if there is a remainder, include
                # one last partial vector or mMatrix message
                if remainder != 0:
                    last_idx_chunk.append(arg.size)

                # Append the results
                md.append((abbrev + str(idx) + "-messages", str(len(last_idx_chunk))))
                chunks.append(last_idx_chunk)

            else:
                # Otherwise deal with a single message... Append results.
                md.append((abbrev + str(idx) + "-messages", str(1)))
                chunks.append([arg.size])

            # Increase idx by 1
            idx += 1

        # Return the metadata and the chunks list for each vector or matrix
        return md, chunks

    def _generate_vector_stream(self, chunks: "list[list[int]]", *args: np.ndarray):
        # Loop over all input arguments
        for arg, vector_chunks in zip(args, chunks):
            # Perform some argument input sanity checks
            self._sanity_check_vector(arg)

            # If sanity checks are fine... yield the corresponding vector message
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
            # Perform some argument input sanity checks.
            self._sanity_check_matrix(arg)

            # If sanity checks are fine... yield the corresponding matrix message
            #
            # When dealing with matrices, ravel it to a 1D array (avoids copy)
            arg_as_vec = arg.ravel()

            # Loop over the chunk indices
            processed_idx = 0
            for last_idx_chunk in matrix_chunks:
                # Use tmp_idx in yield function and update the processed_idx afterwards
                tmp_idx = processed_idx
                processed_idx = last_idx_chunk

                # Yield
                yield grpcdemo_pb2.Matrix(
                    data_type=constants.NP_DTYPE_TO_DATATYPE[arg.dtype.type],
                    matrix_rows=arg.shape[0],
                    matrix_cols=arg.shape[1],
                    matrix_as_chunk=arg_as_vec[tmp_idx:last_idx_chunk].tobytes(),
                )

    def _read_nparray_from_vector(self, response_iterator):
        # Get the metadata
        response_md = response_iterator.initial_metadata()

        # Parse the server's metadata
        full_msg, chunks_per_msg = self._parse_server_metadata(response_md)

        # Initialize the output list
        resulting_vectors = []

        # Start processing messages independently
        for msg in range(full_msg):
            # Init the resulting numpy.ndarray to None, its size and its type
            result = None
            result_size = 0
            result_dtype = None

            # Loop over the available chunks per message
            for chunk_idx in range(chunks_per_msg[msg]):
                # Read a message
                vector = next(response_iterator)

                # If it is the first chunk being processed, parse dtype and size
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

            # Check if the final vector has the desired size
            if result.size != result_size:
                raise RuntimeError("Problems reading server full Vector message...")
            else:
                # If everything is fine, append to resulting_vectors list
                resulting_vectors.append(result)

        # Return the resulting_vectors list
        return resulting_vectors

    def _read_nparray_from_matrix(self, response_iterator):
        # Get the metadata
        response_md = response_iterator.initial_metadata()

        # Parse the server's metadata
        full_msg, chunks_per_msg = self._parse_server_metadata(response_md)

        # Initialize the output list
        resulting_matrices = []

        # Start processing messages independently
        for msg in range(full_msg):
            # Init the resulting numpy.ndarray to None, its size (rows,cols), and its type
            result = None
            result_rows = 0
            result_cols = 0
            result_dtype = None

            # Loop over the available chunks per message
            for chunk_idx in range(chunks_per_msg[msg]):
                # Read a message
                matrix = next(response_iterator)

                # If it is the first chunk being processing, parse dtype and size (rows,cols)
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

            # Check if the final matrix has the desired size
            if result.size != result_rows * result_cols:
                raise RuntimeError("Problems reading server full matrix message...")
            else:
                # If everything is fine, append to resulting_matrices list
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
        # Perform some argument input sanity checks.
        if type(arg) is not np.ndarray:
            raise RuntimeError("Invalid argument. Only numpy.ndarrays are allowed.")
        elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
            raise RuntimeError(
                "Invalid argument. Only numpy.ndarrays of type int32 and float64 are allowed."
            )
        elif arg.ndim != 1:
            raise RuntimeError("Invalid argument. Only 1D numpy.ndarrays are allowed.")

    def _sanity_check_matrix(self, arg):
        # Perform some argument input sanity checks.
        if type(arg) is not np.ndarray:
            raise RuntimeError("Invalid argument. Only numpy.ndarrays are allowed.")
        elif arg.dtype.type not in constants.NP_DTYPE_TO_DATATYPE.keys():
            raise RuntimeError(
                "Invalid argument. Only numpy.ndarrays of type int32 and float64 are allowed."
            )
        elif arg.ndim != 2:
            raise RuntimeError("Invalid argument. Only 2D numpy.ndarrays are allowed.")

    def _parse_server_metadata(self, response_md: "list[tuple]"):
        # Init the return variables: amount of full messages received
        # and partial messages per full message
        full_msg = 0
        chunks_per_msg = []

        # Find out how many full messages are to be processed
        for md in response_md:
            if md[0] == "full-vectors" or md[0] == "full-matrices":
                full_msg = int(md[1])

        # Identify the chunks per message (only if successful previously)
        if full_msg != 0:
            for i in range(1, full_msg + 1):
                for md in response_md:
                    if md[0] == "vec%d-messages" % i or md[0] == "mat%d-messages" % i:
                        chunks_per_msg.append(int(md[1]))

        return full_msg, chunks_per_msg
