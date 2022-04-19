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


@pytest.mark.skip(reason="Not valid yet")
def test_add_vectors_with_grpc(grpc_stub):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_add = client.add_vectors(vec_1, vec_2)
    np.testing.assert_allclose(vec_add, np.array([6, 6, 5, 4]))
