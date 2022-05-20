import pytest

from eigen_cpp_client import GRPCClient

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator

# ================================================================================
# Unit tests for client-server interaction
# ================================================================================


@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_grpc(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two lists (as vectors). Calling the C++
    implementation of the client and server."""

    client = GRPCClient("0.0.0.0", 50000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_grpc(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two lists (as vectors). Calling the C++
    implementation of the client and server."""

    client = GRPCClient("0.0.0.0", 50000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_grpc(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two lists (as matrices). Calling the C++
    implementation of the client and server."""

    client = GRPCClient("0.0.0.0", 50000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add_matrices, mat_1, mat_2)


@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_grpc(benchmark, grpc_stub, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two lists (as matrices). Calling the C++
    implementation of the client and server."""

    client = GRPCClient("0.0.0.0", 50000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply_matrices, mat_1, mat_2)
