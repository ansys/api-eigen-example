import numpy as np
import pytest

from ansys.eigen.python.grpc.client import DemoGRPCClient

# ================================================================================
# Point your stubs and service to test the client-server interaction
#
# These fixtures will provide us with the capability of doing client-server tests
# ================================================================================


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from ansys.eigen.python.grpc.generated.grpcdemo_pb2_grpc import (
        add_GRPCDemoServicer_to_server,
    )

    return add_GRPCDemoServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from ansys.eigen.python.grpc.server import GRPCDemoServicer

    return GRPCDemoServicer()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    from ansys.eigen.python.grpc.generated.grpcdemo_pb2_grpc import GRPCDemoStub

    return GRPCDemoStub(grpc_channel)


# ================================================================================
# Unit tests for client-server interaction
# ================================================================================


def test_add_vectors(benchmark, grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    benchmark(client.add_vectors, vec_1, vec_2)


def test_multiply_vectors(benchmark, grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    benchmark(client.multiply_vectors, vec_1, vec_2)


def test_add_matrices(benchmark, grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""

    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    benchmark(client.add_matrices, mat_1, mat_2)


def test_multiply_matrices(benchmark, grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    benchmark(client.multiply_matrices, mat_1, mat_2)
