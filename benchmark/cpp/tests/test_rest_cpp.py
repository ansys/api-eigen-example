import pytest

from eigen_cpp_client import RESTClient

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator


@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_rest_cpp(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two lists (as vectors). Calling the C++
    implementation of the client and server."""
    client = RESTClient("http://0.0.0.0:18080")

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_rest_cpp(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two lists (as vectors). Calling the C++
    implementation of the client and server."""
    client = RESTClient("http://0.0.0.0:18080")

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply_vectors, vec_1, vec_2)


@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_rest_cpp(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two lists (as matrices). Calling the C++
    implementation of the client and server."""
    client = RESTClient("http://0.0.0.0:18080")

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add_matrices, mat_1, mat_2)


@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_rest_cpp(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two lists (as matrices). Calling the C++
    implementation of the client and server."""
    client = RESTClient("http://0.0.0.0:18080")

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply_matrices, mat_1, mat_2)
