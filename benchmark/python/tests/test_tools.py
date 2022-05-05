""" Tools for BM tests """

from random import random, seed

import numpy as np

# MIN and MAX values for our random numbers
MIN = 0.0
MAX = 10.0

# The amount of sizes of numpy.ndarrays to be processed
SIZES = [pow(2, n) for n in range(1, 8)]
SIZES_IDS = [f'{i:05d}' for i in SIZES]

# Initialize our seed
seed(1)

# Create the random value generator
def gen_value():
    return MIN + (random() * (MAX - MIN))


# Auxiliary function to generate random vectors
def vec_generator(vec_length):
    return np.array([gen_value() for _ in range(0, vec_length)], dtype=np.float64)


# Auxiliary function to generate random square matrices
def mat_generator(mat_size):
    return np.array(
        [[gen_value() for _ in range(0, mat_size)] for _ in range(0, mat_size)],
        dtype=np.float64,
    )
