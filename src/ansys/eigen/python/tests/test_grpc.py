import numpy as np
import pytest

from ansys.eigen.python.grpc.client import DemoGRPCClient
from ansys.eigen.python.tests.test_tools import (
    SIZES,
    SIZES_IDS,
    mat_generator,
    vec_generator,
)

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


def test_greeting(capsys, grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing a simple greeting request."""

    client = DemoGRPCClient(test=grpc_stub)

    client.request_greeting("Michael")

    captured = capsys.readouterr()
    assert (
        captured.out
        == "Greeting requested! Requested by: Michael\nSize of message: 96B\nThe server answered: Hello, Michael!\n"
    )


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_flip_vector(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing a simple vector-flipping request."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)

    vec_flip = client.flip_vector(vec_1)

    np.testing.assert_allclose(vec_flip, np.flip(vec_1))


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    vec_add = client.add_vectors(vec_1, vec_2)
    np.testing.assert_allclose(vec_add, vec_1 + vec_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_four_vectors(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing the addition of four numpy arrays (as vectors).

    This is only possible with the gRPC demo."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)
    vec_3 = vec_generator(sz)
    vec_4 = vec_generator(sz)

    vec_add = client.add_vectors(vec_1, vec_2, vec_3, vec_4)
    np.testing.assert_allclose(vec_add, vec_1 + vec_2 + vec_3 + vec_4)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    vec_mult = client.multiply_vectors(vec_1, vec_2)
    np.testing.assert_allclose(vec_mult, vec_1.dot(vec_2))


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""

    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    mat_add = client.add_matrices(mat_1, mat_2)

    np.testing.assert_allclose(mat_add, mat_1 + mat_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices(grpc_stub, sz):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    mat_mult = client.multiply_matrices(mat_1, mat_2)

    np.testing.assert_allclose(mat_mult, np.matmul(mat_1, mat_2))
