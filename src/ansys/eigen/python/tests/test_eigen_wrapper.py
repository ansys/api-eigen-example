import demo_eigen_wrapper
import numpy as np


def test_function():

    # Testing adding vectors using the wrapper

    array_1 = np.array([1, 2, 3, 4], dtype=np.float64)
    array_2 = np.array([5, 4, 2, 0], dtype=np.float64)
    array_3 = demo_eigen_wrapper.add_vectors(array_1, array_2)

    assert array_3[0] == 6
    assert array_3[1] == 6
    assert array_3[2] == 5
    assert array_3[3] == 4

    # Testing multiplying vectors using the wrapper (dot product)

    array_3 = demo_eigen_wrapper.multiply_vectors(array_1, array_2)

    assert array_3 == 19

    # Testing adding matrices using the wrapper

    mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
    mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

    mat_3 = demo_eigen_wrapper.add_matrices(mat_1, mat_2)

    assert mat_3[0, 0] == 6
    assert mat_3[0, 1] == 6
    assert mat_3[1, 0] == 5
    assert mat_3[1, 1] == 4

    # Testing multiplying matrices using the wrapper

    mat_3 = demo_eigen_wrapper.multiply_matrices(mat_1, mat_2)

    assert mat_3[0, 0] == 9
    assert mat_3[0, 1] == 4
    assert mat_3[1, 0] == 23
    assert mat_3[1, 1] == 12
