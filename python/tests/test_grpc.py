import numpy as np
import pytest

from python.grpc.client import DemoGRPCClient

# ================================================================================
# Point your stubs and service to test the client-server interaction
#
# These fixtures will provide us with the capability of doing client-server tests
# ================================================================================


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from python.grpc.generated.grpcdemo_pb2_grpc import add_GRPCDemoServicer_to_server

    return add_GRPCDemoServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from python.grpc.server import GRPCDemoServicer

    return GRPCDemoServicer()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    from python.grpc.generated.grpcdemo_pb2_grpc import GRPCDemoStub

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
    assert captured.out == "The server answered: Hello, Michael!\n"


def test_flip_vector(grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing a simple vector-flipping request."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)

    vec_flip = client.flip_vector(vec_1)

    np.testing.assert_allclose(vec_flip, np.flip(vec_1))


def test_add_vectors(grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_add = client.add_vectors(vec_1, vec_2)
    np.testing.assert_allclose(vec_add, np.array([6, 6, 5, 4]))
    
def test_add_four_vectors(grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the addition of four numpy arrays (as vectors).
    
    This is only possible with the gRPC demo."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)
    vec_3 = np.array([-5, -4, -2, 0], dtype=np.float64)
    vec_4 = np.array([-1, -2, -3, -4], dtype=np.float64)

    vec_add = client.add_vectors(vec_1, vec_2, vec_3, vec_4)
    np.testing.assert_allclose(vec_add, np.array([0., 0., 0., 0.]))

def test_multiply_vectors(grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_mult = client.multiply_vectors(vec_1, vec_2)
    np.testing.assert_allclose(vec_mult, np.array([19.0]))
