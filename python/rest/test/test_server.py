import json
import numpy as np
import pytest
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


def test_server_ops_vectors(testing_client):
    """Unit test to verify that the server returns the expected response
    when performing the addition and multiplication of two numpy arrays (as vectors)."""

    vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

    response_1 = testing_client.post("/Vectors", json={"value": vec_1.tolist()})
    response_2 = testing_client.post("/Vectors", json={"value": vec_2.tolist()})

    assert response_1.status_code == 201
    id_1 = json.loads(response_1.text)["vector"]["id"]
    assert response_2.status_code == 201
    id_2 = json.loads(response_2.text)["vector"]["id"]

    response_add = testing_client.get("/add/Vectors", json={"id1": id_1, "id2": id_2})
    assert response_add.status_code == 200
    value = json.loads(json.loads(response_add.text)["vector-addition"]["result"])

    assert value[0] == 6
    assert value[1] == 6
    assert value[2] == 5
    assert value[3] == 4

    response_mul = testing_client.get(
        "/multiply/Vectors", json={"id1": id_1, "id2": id_2}
    )
    assert response_mul.status_code == 200
    value = json.loads(json.loads(response_mul.text)["vector-multiplication"]["result"])

    assert value == 19


def test_server_ops_matrices(testing_client):
    """Unit test to verify that the server returns the expected response
    when performing the addition and multiplication of two numpy arrays (as matrices)."""

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    response_1 = testing_client.post("/Matrices", json={"value": mat_1.tolist()})
    response_2 = testing_client.post("/Matrices", json={"value": mat_2.tolist()})

    assert response_1.status_code == 201
    id_1 = json.loads(response_1.text)["matrix"]["id"]
    assert response_2.status_code == 201
    id_2 = json.loads(response_2.text)["matrix"]["id"]

    response_add = testing_client.get("/add/Matrices", json={"id1": id_1, "id2": id_2})
    assert response_add.status_code == 200
    value = json.loads(json.loads(response_add.text)["matrix-addition"]["result"])

    assert value[0][0] == 6
    assert value[0][1] == 6
    assert value[1][0] == 5
    assert value[1][1] == 4

    response_mul = testing_client.get(
        "/multiply/Matrices", json={"id1": id_1, "id2": id_2}
    )
    assert response_mul.status_code == 200
    value = json.loads(json.loads(response_mul.text)["matrix-multiplication"]["result"])

    assert value[0][0] == 9
    assert value[0][1] == 4
    assert value[1][0] == 23
    assert value[1][1] == 12
