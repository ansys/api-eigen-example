import numpy as np
import pytest

from python.rest.client import DemoRESTClient
from python.rest.server import create_app


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


def test_client_add_vectors(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_add = client.add(vec_1, vec_2)
    np.testing.assert_allclose(vec_add, np.array([6, 6, 5, 4]))


def test_client_subtract_vectors(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the subtraction of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_subt = client.subtract(vec_1, vec_2)

    np.testing.assert_allclose(vec_subt, np.array([-4, -2, 1, 4]))


def test_client_multiply_vectors(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    vec_mult = client.multiply(vec_1, vec_2)

    assert vec_mult == 19


def test_client_add_matrices(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_add = client.add(mat_1, mat_2)

    np.testing.assert_allclose(mat_add, np.array([[6, 6], [5, 4]]))


def test_client_subtract_matrices(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the subtraction of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_subt = client.subtract(mat_1, mat_2)

    np.testing.assert_allclose(mat_subt, np.array([[-4, -2], [1, 4]]))


def test_client_multiply_matrices(testing_client):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_mult = client.multiply(mat_1, mat_2)

    np.testing.assert_allclose(mat_mult, np.array([[9,4], [23, 12]]))


def test_client_connection_details(capsys, testing_client):
    """Unit test to verify that the client connection details are shown as expected."""
    client = DemoRESTClient("http://127.0.0.1", 5000, user="myUser", pwd="myPwd")
    client.get_connection_details()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Connection to host http://127.0.0.1 through port 5000 "
        + "for using the demo-eigen-wrapper package as a REST Service.\n"
        + ">>> User: myUser\n"
        + ">>> Pwd: myPwd\n"
    )

    client = DemoRESTClient("http://127.0.0.1", 5000, user="myUser")
    client.get_connection_details()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Connection to host http://127.0.0.1 through port 5000 "
        + "for using the demo-eigen-wrapper package as a REST Service.\n"
        + ">>> User: myUser\n"
    )

    client = DemoRESTClient("http://127.0.0.1", 5000)
    client.get_connection_details()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Connection to host http://127.0.0.1 through port 5000 "
        + "for using the demo-eigen-wrapper package as a REST Service.\n"
    )

    test_client = DemoRESTClient(None, None, client=testing_client)
    test_client.get_connection_details()
    captured = capsys.readouterr()
    assert captured.out == "Using a test client. Unnecessary info.\n"


def test_client_errors(testing_client):
    """Unit test to verify multiple client error conditions."""
    client = DemoRESTClient(None, None, client=testing_client)
    error_client = DemoRESTClient("http://127.0.0.1", 5000)

    # Test 1: Check that as input arguments, a numpy.ndarray is given (for arg1)
    with pytest.raises(RuntimeError) as e_info:
        client.add("myArg1", "myArg2")
        assert (
            str(e_info.value)
            == "First argument is not a numpy.ndarray of dtype numpy.float64. Check inputs."
        )

    # Test 2: Check that as input arguments, a numpy.ndarray is given (for arg2)
    with pytest.raises(RuntimeError) as e_info:
        client.add(np.empty(0), "myArg2")
        assert (
            str(e_info.value)
            == "Second argument is not a numpy.ndarray of dtype numpy.float64. Check inputs."
        )

    # Test 3: Check that as input arguments, a numpy.ndarray of dtype float64 is given (for arg2)
    with pytest.raises(RuntimeError) as e_info:
        client.add(np.empty(0, dtype=np.int64), "myArg2")
        assert (
            str(e_info.value)
            == "First argument is not a numpy.ndarray of dtype numpy.float64. Check inputs."
        )

    # Test 4: Check that as input arguments, the numpy arrays have different shapes
    with pytest.raises(RuntimeError) as e_info:
        client.add(np.empty(0), np.empty(2))
        assert str(e_info.value) == "Arguments have different shapes. Check inputs."

    # Test 5: Check that as input arguments, the numpy arrays have invalid dimensions (0 or +2 dims)
    with pytest.raises(RuntimeError) as e_info:
        client.add(np.ones(shape=(3, 2, 1)), np.ones(shape=(3, 2, 1)))
        assert (
            str(e_info.value)
            == "Only numpy.ndarrays of 1D (i.e. vectors) or 2D (i.e. matrices) are allowed. Check inputs."
        )
        client.add(np.ones(shape=()), np.ones(shape=()))
        assert (
            str(e_info.value)
            == "Only numpy.ndarrays of 1D (i.e. vectors) or 2D (i.e. matrices) are allowed. Check inputs."
        )

    # Test 6 : Check that whenever trying to connect to an invalid client, the correct error is retrieved
    with pytest.raises(RuntimeError) as e_info:
        error_client.add(np.ones(shape=(3, 2)), np.ones(shape=(3, 2)))
        assert (
            str(e_info.value)
            == "Could not connect to server... Check server status or connection details."
        )
        # Test unreachable function otherwise by accessing it directly... the previous operation
        # is going to fail in the __post_resource(...) method.
        error_client.__get_ops_resource(1, 2, "add", "Vectors")
        assert (
            str(e_info.value)
            == "Could not connect to server... Check server status or connection details."
        )
