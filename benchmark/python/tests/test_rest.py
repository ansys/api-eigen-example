import pytest

from ansys.eigen.python.rest.client import DemoRESTClient
from ansys.eigen.python.rest.server import create_app

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator


@pytest.fixture(scope="module")
def testing_client():
    # Create the app
    app = create_app()
    app.testing = True

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_rest(benchmark, testing_client, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add, vec_1, vec_2)

@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_rest(benchmark, testing_client, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply, vec_1, vec_2)

@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_rest(benchmark, testing_client, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add, mat_1, mat_2)

@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_rest(benchmark, testing_client, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply, mat_1, mat_2)
