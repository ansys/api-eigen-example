# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import pytest

from ansys.eigen.python.rest.client import DemoRESTClient
from ansys.eigen.python.rest.server import create_app
from ansys.eigen.python.testing.test_tools import (
    SIZES,
    SIZES_IDS,
    mat_generator,
    vec_generator,
)


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


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_add_vectors_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    vec_add = client.add(vec_1, vec_2)
    np.testing.assert_allclose(vec_add, vec_1 + vec_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_subtract_vectors_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the subtraction of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    vec_subt = client.subtract(vec_1, vec_2)

    np.testing.assert_allclose(vec_subt, vec_1 - vec_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_multiply_vectors_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient(None, None, client=testing_client)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    vec_mult = client.multiply(vec_1, vec_2)

    np.testing.assert_allclose(vec_mult, vec_1.dot(vec_2))


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_add_matrices_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    mat_add = client.add(mat_1, mat_2)

    np.testing.assert_allclose(mat_add, mat_1 + mat_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_subtract_matrices_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the subtraction of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    mat_subt = client.subtract(mat_1, mat_2)

    np.testing.assert_allclose(mat_subt, mat_1 - mat_2)


@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_client_multiply_matrices_rest_cli(testing_client, sz):
    """Unit test to verify that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient(None, None, client=testing_client)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    mat_mult = client.multiply(mat_1, mat_2)

    np.testing.assert_allclose(mat_mult, np.matmul(mat_1, mat_2))


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


def test_client_errors_rest(testing_client):
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
