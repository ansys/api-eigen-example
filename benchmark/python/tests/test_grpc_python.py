import pytest

from ansys.eigen.python.grpc.client import DemoGRPCClient

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator

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


@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_grpc_python(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_grpc_python(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""

    client = DemoGRPCClient(test=grpc_stub)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_grpc_python(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""

    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add_matrices, mat_1, mat_2)


@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_grpc_python(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoGRPCClient(test=grpc_stub)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply_matrices, mat_1, mat_2)
