import pytest

from ansys.eigen.python.rest.client import DemoRESTClient

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator


@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add, vec_1, vec_2)


@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply, vec_1, vec_2)


@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add, mat_1, mat_2)


@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply, mat_1, mat_2)
