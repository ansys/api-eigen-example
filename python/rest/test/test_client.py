import numpy as np

from python.rest.client import DemoRESTClient

# If you just run these tests... it will crash, for sure.
#
# At the moment, you have to deploy manually the server first. From the root directory
# of the project run:
#
# $ export FLASK_APP=python/rest/server.py
# $ flask run
#
# And then you will be able to run these tests successfully


def test_client_add_vectors():
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_add = client.add(vec_1, vec_2)

    assert vec_add[0] == 6
    assert vec_add[1] == 6
    assert vec_add[2] == 5
    assert vec_add[3] == 4


def test_client_substract_vectors():
    """Unit test to verify that the client gets the expected response
    when performing the substraction of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_subst = client.substract(vec_1, vec_2)

    assert vec_subst[0] == -4
    assert vec_subst[1] == -2
    assert vec_subst[2] == 1
    assert vec_subst[3] == 4


def test_client_multiply_vectors():
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_mult = client.multiply(vec_1, vec_2)

    assert vec_mult == 19


def test_client_add_matrices():
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_add = client.add(mat_1, mat_2)

    assert mat_add[0, 0] == 6
    assert mat_add[0, 1] == 6
    assert mat_add[1, 0] == 5
    assert mat_add[1, 1] == 4


def test_client_substract_matrices():
    """Unit test to verify that the client gets the expected response
    when performing the substraction of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_subst = client.substract(mat_1, mat_2)

    assert mat_subst[0, 0] == -4
    assert mat_subst[0, 1] == -2
    assert mat_subst[1, 0] == 1
    assert mat_subst[1, 1] == 4


def test_client_multiply_matrices():
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://127.0.0.1", 5000)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_mult = client.multiply(mat_1, mat_2)

    assert mat_mult[0, 0] == 9
    assert mat_mult[0, 1] == 4
    assert mat_mult[1, 0] == 23
    assert mat_mult[1, 1] == 12
