"""The Python implementation of the gRPC API Eigen example server."""

from concurrent import futures
import logging

import demo_eigen_wrapper
import grpc
import numpy as np

import python.grpc.constants as constants
import python.grpc.generated.grpcdemo_pb2 as grpcdemo_pb2
import python.grpc.generated.grpcdemo_pb2_grpc as grpcdemo_pb2_grpc


def check_data_type(type, new_type):
    """Auxiliary method to check if the new data type is the same as the previous one or not.

    Parameters
    ----------
    type : numpy.type
        The type of the numpy arrays processed.
    new_type : numpy.type
        The type of the numpy array being processed.

    Returns
    -------
    numpy.type
        The type of the numpy array.

    Raises
    ------
    RuntimeError
        In case there is already a type, and it does not match that of the new_type argument.
    """
    if type is None:
        return new_type
    elif type != new_type:
        raise RuntimeError(
            "Error while processing data types... Input arguments are of different nature (i.e. int32, float64)."
        )
    else:
        return type


def check_size(size, new_size):
    """Auxiliary method to check if the new parsed size is the same as the previous one or not.

    Parameters
    ----------
    size : tuple
        The size of the numpy arrays processed.
    new_size : _type_
        The size of the numpy array being processed.

    Returns
    -------
    tuple
        The size of the numpy array.

    Raises
    ------
    RuntimeError
        In case there is already a size, and it does not match that of the new_size argument.
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
    """Provides methods that implement functionality of API Eigen Example server."""

    def __init__(self) -> None:
        """No special init is required for the server... Unless we wanted to store the data in a DB. This is to be determined."""
        # TODO : is it required to store the input vectors in a DB?
        super().__init__()

    def SayHello(self, request, context):
        """Greeter method - to test if the server works correctly and is up and running.

        Parameters
        ----------
        request : HelloRequest
            The greeting request send by the client.
        context : grpc.ServicerContext
            Provides RPC-specific information.

        Returns
        -------
        grpcdemo_pb2.HelloReply
            The greeting reply by the server.
        """
        return grpcdemo_pb2.HelloReply(message="Hello, %s!" % request.name)

    def FlipVector(self, request, context):
        """Simple flipping method which inverts a given Vector.

        Parameters
        ----------
        request : grpcdemo_pb2.Vector
            The input Vector message.
        context : grpc.ServicerContext
            Provides RPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            The flipped Vector message.
        """
        # Check the data type of the incoming vector
        type = None
        size = None
        if request.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
            type = check_data_type(type, np.int32)
        elif request.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
            type = check_data_type(type, np.float64)

        # Check the size of the incoming vector
        size = check_size(size, (request.vector_size,))

        # Deserialize the numpy array
        nparray = np.frombuffer(request.vector_as_chunk, dtype=type)

        # Flip it
        nparray_flipped = np.flip(nparray)

        # Finally, return the Vector message
        return grpcdemo_pb2.Vector(
            data_type=constants.NP_DTYPE_TO_DATATYPE[type],
            vector_size=size[0],
            vector_as_chunk=nparray_flipped.tobytes(),
        )

    def AddVectors(self, request_iterator, context):
        """gRPC method for allowing the addition of Vectors.

        Parameters
        ----------
        request_iterator : iterator
            An iterator to the stream of Vector messages provided.
        context : grpc.ServicerContext
            Provides RPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            The Vector message.
        """
        # Process the input messages
        type, size, vector_list = self._get_vectors(request_iterator)

        # Create an empty array with the input arguments characteristics (dtype, size)
        result = np.empty(size, dtype=type)

        # Add all provided vectors using the Eigen library
        for vector in vector_list:
            result = demo_eigen_wrapper.add_vectors(result, vector)

        # Finally, return the Vector message
        return grpcdemo_pb2.Vector(
            data_type=constants.NP_DTYPE_TO_DATATYPE[type],
            vector_size=size[0],
            vector_as_chunk=result.tobytes(),
        )

    def MultiplyVectors(self, request_iterator, context):
        """gRPC method for allowing the dot product of Vectors (only 2 Vectors allowed).

        Parameters
        ----------
        request_iterator : iterator
            An iterator to the stream of Vector messages provided.
        context : grpc.ServicerContext
            Provides RPC-specific information.

        Returns
        -------
        grpcdemo_pb2.Vector
            The Vector message.
        """
        # Process the input messages
        type, _, vector_list = self._get_vectors(request_iterator)

        # Check that the Vector list contains a maximum of two vectors
        if len(vector_list) != 2:
            raise RuntimeError(
                "Unexpected number of vectors to be multiplied: "
                + len(vector_list)
                + ". Only 2 is valid."
            )

        # Perform the dot product of the provided vectors using the Eigen library
        result = demo_eigen_wrapper.multiply_vectors(*vector_list)
        result = np.array(result, dtype=type)

        # Finally, return the Vector message
        return grpcdemo_pb2.Vector(
            data_type=constants.NP_DTYPE_TO_DATATYPE[type],
            vector_size=1,
            vector_as_chunk=result.tobytes(),
        )

    def AddMatrices(self, request_iterator, context):
        # TODO : Implement AddMatrices server logic
        return super().AddMatrices(request_iterator, context)

    def MultiplyMatrices(self, request_iterator, context):
        # TODO : Implement MultiplyMatrices server logic
        return super().MultiplyMatrices(request_iterator, context)

    def _get_vectors(self, request_iterator):
        """Private method to process a stream of Vector messages.

        Parameters
        ----------
        request_iterator : iterator
            An iterator to the received request messages of type Vector.

        Returns
        -------
        np.type, tuple, list of np.array
            The type of data, the size of the vectors and the list of vectors to be processed.
        """
        # Initialize the auxiliary variables and output vector list
        type = None
        size = None
        vector_list = []

        # Iterate over all incoming vectors
        for vector in request_iterator:
            # Check the data type of the incoming vector
            if vector.data_type == grpcdemo_pb2.DataType.Value("INTEGER"):
                type = check_data_type(type, np.int32)
            elif vector.data_type == grpcdemo_pb2.DataType.Value("DOUBLE"):
                type = check_data_type(type, np.float64)

            # Check the size of the incoming vector
            size = check_size(size, (vector.vector_size,))

            # Deserialize the numpy array
            nparray = np.frombuffer(vector.vector_as_chunk, dtype=type)
            # nparray.reshape(size) ---> This is to be used for matrices only

            # Add the array to the list
            vector_list.append(nparray)

        # Return the input vector list (as a list of numpy.ndarray)
        return type, size, vector_list


def serve():
    """Provides method to deploy the API Eigen Example server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcdemo_pb2_grpc.add_GRPCDemoServicer_to_server(GRPCDemoServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
