# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

""" Tools for BM tests """

from random import random, seed

import numpy as np

# Modifiable parameter -- NVALUES
#
# This parameter defines the amount of runs (and consequently, powers of 2)
# which will define the size of our arrays.. See below, SIZES
NVALUES = 12

# ==================================================================================
# IT IS NOT RECOMMENDED TO MODIFY THE SCRIPT BEYOND THIS POINT WITHOUT KNOWLEDGE
# OF HOW THE BENCHMARK TESTS ARE RUN. USE WITH CAUTION...
# ==================================================================================


# MIN and MAX values for our random numbers
MIN = 0.0
MAX = 10.0

# The amount of sizes of numpy.ndarrays to be processed
SIZES = [pow(2, n) for n in range(1, NVALUES)]
SIZES_IDS = [f"{i:05d}" for i in SIZES]  # noqa: E231

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


# Auxiliary function to generate random vectors (as a list)
def vec_generator_list(vec_length):
    return [gen_value() for _ in range(0, vec_length)]


# Auxiliary function to generate random square matrices (as a list)
def mat_generator_list(mat_size):
    return [[gen_value() for _ in range(0, mat_size)] for _ in range(0, mat_size)]
