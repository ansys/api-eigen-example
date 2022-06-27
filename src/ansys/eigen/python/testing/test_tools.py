"""Tools for tests """

from random import random, seed

import numpy as np

# Modifiable parameter -- NVALUES
#
# This parameter defines the number of runs (and consequently, powers of 2)
# that define the size of arrays. See SIZES below.
NVALUES = 12

# ==================================================================================
# YOU SHOULD NOT MODIFY THE SCRIPT BEYOND THIS POINT WITHOUT KNOWLEDGE
# OF HOW THE TESTS ARE RUN. USE WITH CAUTION...
# ==================================================================================

# MIN and MAX values for random numbers
MIN = 0.0
MAX = 10.0

# The amount of sizes of numpy.ndarrays to be processed
SIZES = [pow(2, n) for n in range(1, NVALUES)]
SIZES_IDS = [f"{i:05d}" for i in SIZES]


# Initialize the seed
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
