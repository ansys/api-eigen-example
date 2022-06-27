"""Python implementation of the gRPC API Eigen example server."""

from concurrent import futures
import logging

import click
import demo_eigen_wrapper
import grpc
import numpy as np

import ansys.eigen.python.grpc.constants as constants
import ansys.eigen.python.grpc.generated.grpcdemo_pb2 as grpcdemo_pb2
import ansys.eigen.python.grpc.generated.grpcdemo_pb2_grpc as grpcdemo_pb2_grpc

# =================================================================================================
# AUXILIARY METHODS for Server operations
# =================================================================================================


def check_data_type(dtype, new_dtype):
    """Check if the new data type is the same as the previous data type.

    Parameters
    ----------
    dtype : numpy.type
        Type of the numpy array before processing.
    new_dtype : numpy.type
        Type of the numpy array to be processed.

    Returns
    -------
    numpy.type
        Type of the numpy array.

    Raises
    ------
    RuntimeError
        In case there is already a type and it does not match that of the new_type argument.
    """
    if dtype is None:
        return new_dtype
    elif dtype != new_dtype:
        raise RuntimeError(
            "Error while processing data types... Input arguments are of different nature (such as int32, float64)."
        )
    else:
        return dtype


def check_size(size, new_size):
    """Check if the new parsed size is the same as the previous size.

    Parameters
    ----------
    size : tuple
        Size of the numpy array before processing.
    new_size : _type_
        Size of the numpy array to process.

    Returns
    -------
    tuple
        Size of the numpy array.

    Raises
    ------
    RuntimeError
        In case there is already a size and it does not match that of the new_size argument.
    """
    if size is None:
        return new_size
    elif size != new_size:
        raise RuntimeError(
            "Error while processing data types... Input arguments are of different sizes."
        )
    else:
        return size


class GRPCDemoServicer(grpcdemo_pb2_grpc.GRPCDemoServicer):
    """Provides methods that implement functionality of the API Eigen Example server."""

    def __init__(self) -> None:
        """No special init is required for the server... unless data is to be stored in a DB. This is to be determined."""
        # TODO : is it required to store the input vectors in a DB?
        super().__init__()

    # =================================================================================================
    # PUBLIC METHODS for Server operations
    # =================================================================================================

    def SayHello(self, request, context):
        """Test the greeter method to see if the server is up and running correctly.

        Parameters
        ----------
        request : HelloRequest
            Greeting request sent by the client.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.HelloReply
           Reply to greeting by the server.
        """
        click.echo("Greeting requested! Requested by: " + request.name)

        # Inform about the size of the message content
        click.echo("Size of message: " + constants.human_size(request))

        return grpcdemo_pb2.HelloReply(message="Hello, %s!" % request.name)

    def FlipVector(self, request_iterator, context):
        """Flip a given vector.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the stream of vector messages provided.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            Flipped vector message.
        """
        click.echo("Vector flip requested.")

        # Process the metadata
        md = self._read_client_metadata(context)

        # Process the input messages
        dtype, size, vector_list = self._get_vectors(request_iterator, md)

        # Flip it --> assuming that only one vector is passed
        nparray_flipped = np.flip(vector_list[0])

        # Send the response
        return self._send_vectors(context, nparray_flipped)

    def AddVectors(self, request_iterator, context):
        """Add vectors.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the stream of vector messages provided.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            Vector message.
        """
        click.echo("Vector addition requested.")
        # Process the metadata
        md = self._read_client_metadata(context)

        # Process the input messages
        dtype, size, vector_list = self._get_vectors(request_iterator, md)

        # Create an empty array with the input arguments characteristics (dtype, size)
        result = np.zeros(size, dtype=dtype)

        # Add all provided vectors using the Eigen library
        for vector in vector_list:
            # Casting is needed due to interface with Eigen library... Not the desired approach,
            # but works. Ideally, wvectors should be passed directly, but errors appear
            cast_vector = np.array(vector, dtype=dtype)
            result = demo_eigen_wrapper.add_vectors(result, cast_vector)

        # Send the response
        return self._send_vectors(context, result)

    def MultiplyVectors(self, request_iterator, context):
        """Multiply two vectors.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the stream of vector messages provided.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            Vector message.
        """
        click.echo("Vector dot product requested)

        # Process the metadata
        md = self._read_client_metadata(context)

        # Process the input messages
        dtype, size, vector_list = self._get_vectors(request_iterator, md)

        # Check that the vctor list contains a maximum of two vectors
        if len(vector_list) != 2:
            raise RuntimeError(
                "Unexpected number of vectors to be multiplied: "
                + len(vector_list)
                + ". Only 2 is valid."
            )

        # Perform the dot product of the provided vectors using the Eigen library
        # casting is needed due to interface with Eigen library... Not the desired approach,
        # but works. Ideally, vectors should be passed directly, but errors appear
        vec_1 = np.array(vector_list[0], dtype=dtype)
        vec_2 = np.array(vector_list[1], dtype=dtype)
        result = demo_eigen_wrapper.multiply_vectors(vec_1, vec_2)

        # Return the result as a numpy.ndarray
        result = np.array(result, dtype=dtype, ndmin=1)

        # Finally, send the response
        return self._send_vectors(context, result)

    def AddMatrices(self, request_iterator, context):
        """Add matrices.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the stream of matrix messages provided.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Matrix
            Matrix message.
        """
        click.echo("Matrix addition requested!")
        # Process the metadata
        md = self._read_client_metadata(context)

        # Process the input messages
        dtype, size, matrix_list = self._get_matrices(request_iterator, md)

        # Create an empty array with the input arguments characteristics (dtype, size)
        result = np.zeros(size, dtype=dtype)

        # Add all provided matrices using the Eigen library
        for matrix in matrix_list:
            # Casting is needed due to interface with Eigen library... Not the desired approach,
            # but works. Ideally, we would want to pass matrix directly, but errors appear
            cast_matrix = np.array(matrix, dtype=dtype)
            result = demo_eigen_wrapper.add_matrices(result, cast_matrix)

        # Send the response
        return self._send_matrices(context, result)

    def MultiplyMatrices(self, request_iterator, context):
        """Multiply two matrices.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the stream of Matrix messages provided.
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Matrix
            Matrix message.
        """
        click.echo("Matrix multiplication requested.")

        # Process the metadata
        md = self._read_client_metadata(context)

        # Process the input messages
        dtype, size, matrix_list = self._get_matrices(request_iterator, md)

        # Check that the matrix list contains a maximum of two matrices
        if len(matrix_list) != 2:
            raise RuntimeError(
                "Unexpected number of matrices to be multiplied: "
                + len(matrix_list)
                + ". You can only multiple two matrices."
            )

        # Due to the previous _get_matrices method, the size of all
        # matrices is the same... check that it is a square matrix. Otherwise, no multiplication
        # is possible
        if size[0] != size[1]:
            raise RuntimeError("Only square matrices are allowed for multiplication.")

        # Perform the matrix multiplication of the provided matrices using the Eigen library
        # Casting is needed due to interface with Eigen library... Not the desired approach,
        # but works. Ideally, vector should be passed directly, but errors appear
        mat_1 = np.array(matrix_list[0], dtype=dtype)
        mat_2 = np.array(matrix_list[1], dtype=dtype)
        result = demo_eigen_wrapper.multiply_matrices(mat_1, mat_2)

        # Finally, send the response
        return self._send_matrices(context, result)

    # =================================================================================================
    # PRIVATE METHODS for Server operations
    # =================================================================================================

    def _get_vectors(self, request_iterator, md: dict):
        """Process a stream of vector messages.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the received request messages of type Vector.
        md : dict
            Metadata provided by the client.

        Returns
        -------
        np.type, tuple, list of np.array
            Type of data, size of the vectors, and list of vectors to process.
        """
        # First, determine how many full vector messages are to be processed
        full_msgs = int(md.get("full-vectors"))

        # Initialize the output vector list and some aux vars
        vector_list = []
        dtype = None
        size = None

        # Loop over the expected full messages
        for msg in range(1, full_msgs + 1):

            # Find out how many partial vector messages constitute this full vector message
            chunks = int(md.get("vec%d-messages" % msg))

            # Initialize the output vector
            vector = None

            # Loop over the expected chunks
            for chunk_msg in range(chunks):
                # Read the vector message
                chunk_vec = next(request_iterator)

                # Inform about the size of the message content
                click.echo(
                    "Size of message: "
                    + constants.human_size(chunk_vec.vector_as_chunk)
                )

                # If processing the first chunk of the message, fill in some data
                if chunk_msg == 0:
                    # Check the data type of the incoming vector
                    if chunk_vec.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
                        dtype = check_data_type(dtype, np.int32)
                    elif chunk_vec.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
                        dtype = check_data_type(dtype, np.float64)

                    # Check the size of the incoming vector
                    size = check_size(size, (chunk_vec.vector_size,))

                # Parse the chunk
                if vector is None:
                    vector = np.frombuffer(chunk_vec.vector_as_chunk, dtype=dtype)
                else:
                    tmp = np.frombuffer(chunk_vec.vector_as_chunk, dtype=dtype)
                    vector = np.concatenate((vector, tmp))

            # Check if the final vector has the desired size
            if vector.size != size[0]:
                raise RuntimeError("Problems reading client full vector message...")
            else:
                # If everything is fine, append to vector_list
                vector_list.append(vector)

        # Return the input vector list (as a list of numpy.ndarray)
        return dtype, size, vector_list

    def _get_matrices(self, request_iterator, md: dict):
        """Process a stream of matrix messages.

        Parameters
        ----------
        request_iterator : iterator
            Iterator to the received request messages of type ``Matrix``.
        md : dict
            Metadata provided by the client.

        Returns
        -------
        np.type, tuple, list of np.array
            Type of data, shape of the matrices, and list of matrices to process.
        """
        # Determine how many full matrix messages are to be processed
        full_msgs = int(md.get("full-matrices"))

        # Initialize the output matrix list and some aux vars
        matrix_list = []
        dtype = None
        size = None

        # Loop over the expected full messages
        for msg in range(1, full_msgs + 1):

            # Find out how many partial matrix messages constitute this full matrix message
            chunks = int(md.get("mat%d-messages" % msg))

            # Initialize the output matrix
            matrix = None

            # Loop over the expected chunks
            for chunk_msg in range(chunks):
                # Read the matrix message
                chunk_mat = next(request_iterator)

                # Inform about the size of the message content
                click.echo(
                    "Size of message: "
                    + constants.human_size(chunk_mat.matrix_as_chunk)
                )

                # If processing the first chunk of the message, fill in some data
                if chunk_msg == 0:
                    # Check the data type of the incoming matrix
                    if chunk_mat.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
                        dtype = check_data_type(dtype, np.int32)
                    elif chunk_mat.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
                        dtype = check_data_type(dtype, np.float64)

                    # Check the size of the incoming matrix
                    size = check_size(
                        size,
                        (
                            chunk_mat.matrix_rows,
                            chunk_mat.matrix_cols,
                        ),
                    )

                # Parse the chunk
                if matrix is None:
                    matrix = np.frombuffer(chunk_mat.matrix_as_chunk, dtype=dtype)
                else:
                    tmp = np.frombuffer(chunk_mat.matrix_as_chunk, dtype=dtype)
                    matrix = np.concatenate((matrix, tmp))

            # Check if the final matrix has the desired size
            if matrix.size != size[0] * size[1]:
                raise RuntimeError("Problems reading client full Matrix message...")
            else:
                # If everything is fine, append to matrix_list
                matrix = np.reshape(matrix, size)
                matrix_list.append(matrix)

        # Return the input matrix list (as a list of numpy.ndarray)
        return dtype, size, matrix_list

    def _read_client_metadata(self, context):
        """Return the metadata as a dictionary.

        Parameters
        ----------
        context : grpc.ServicerContext
            gRPC-specific information.

        Returns
        -------
        dict
            Python-readable metadata in dictionary form.
        """
        metadata = context.invocation_metadata()
        metadata_dict = {}
        for c in metadata:
            metadata_dict[c.key] = c.value

        return metadata_dict

    def _generate_md(self, message_type: str, abbrev: str, *args: np.ndarray):
        """Generate the server metadata sent to the client and determine the number of chunks in which to decompose each message.

        Parameters
        ----------
        message_type : str
            Type of message being sent. Options are``vectors`` and ``matrices``.
        abbrev : str
            Abbreviated form of the message being sent. Options are ``vec`` and ``mat``.

        Returns
        -------
        list[tuple], list[list[int]]
            Metadata to be sent by the server and the chunk indices for the list
            of messages to send.

        Raises
        ------
        RuntimeError
            In case of an invalid use of this function.
        """
        # Initialize the metadata and the chunks list for each full message
        md = []
        chunks = []

        # Find how many arguments are to be transmitted
        md.append(("full-" + message_type, str(len(args))))

        # Loop over all input arguments
        idx = 1
        for arg in args:
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

                # This list provides the last index up to which to
                # process in each partial vector or matrix message
                last_idx_chunk = []
                for i in range(1, bulk_chunks + 1):
                    last_idx_chunk.append(i * max_elems)

                # Take into account that if there is a remainder, 
                # include one last partial vector or matrix message.
                if remainder != 0:
                    last_idx_chunk.append(arg.size)

                # Append the results
                md.append((abbrev + str(idx) + "-messages", str(len(last_idx_chunk))))
                chunks.append(last_idx_chunk)

            else:
                # Otherwise dealing with a single message.. Append results.
                md.append((abbrev + str(idx) + "-messages", str(1)))
                chunks.append([arg.size])

            # Increase idx by 1
            idx += 1

        # Return the metadata and the chunks list for each vector or matrix
        return md, chunks

    def _send_vectors(self, context: grpc.ServicerContext, *args: np.ndarray):
        """Send the response vector messages.

        Parameters
        ----------
        context : grpc.ServicerContext
            gRPC context.
        args : np.ndarray
            Variable size of np.arrays to transmit.

        Yields
        ------
        grpcdemo_pb2.Vector
            Vector messages streamed (full or partial, depending on the metadata)
        """

        # Generate the metadata and info on the chunks
        md, chunks = self._generate_md("vectors", "vec", *args)

        # Send the initial metadata
        context.send_initial_metadata(md)

        # Loop over all input arguments
        for arg, vector_chunks in zip(args, chunks):
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

    def _send_matrices(self, context: grpc.ServicerContext, *args: np.ndarray):
        """Sending the response matrix messages.

        Parameters
        ----------
        context : grpc.ServicerContext
            gRPC context.
        args : np.ndarray
            Variable size of np.arrays to transmit.

        Yields
        ------
        grpcdemo_pb2.Matrix
            Matrix messages streamed (full or partial, depending on the metadata)
        """

        # Generate the metadata and info on the chunks
        md, chunks = self._generate_md("matrices", "mat", *args)

        # Send the initial metadata
        context.send_initial_metadata(md)

        # Loop over all input arguments
        for arg, matrix_chunks in zip(args, chunks):
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


# =================================================================================================
# SERVING METHODS for Server operations
# =================================================================================================


def serve():
    """Deploy the API Eigen Example server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcdemo_pb2_grpc.add_GRPCDemoServicer_to_server(GRPCDemoServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
