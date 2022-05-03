import numpy as np
import pytest

from ansys.eigen.python.rest.client import DemoRESTClient
from ansys.eigen.python.rest.server import create_app


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


def test_add_vectors_rest(benchmark, testing_client):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    benchmark(client.add, vec_1, vec_2)


def test_multiply_vectors_rest(benchmark, testing_client):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    benchmark(client.multiply, vec_1, vec_2)


def test_add_matrices_rest(benchmark, testing_client):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    benchmark(client.add, mat_1, mat_2)


def test_multiply_matrices_rest(benchmark, testing_client):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    benchmark(client.multiply, mat_1, mat_2)
