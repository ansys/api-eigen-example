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

import pytest

from ansys.eigen.python.rest.client import DemoRESTClient

from .test_tools import SIZES, SIZES_IDS, mat_generator, vec_generator


@pytest.mark.benchmark(group="add_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_vectors_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.add, vec_1, vec_2)


@pytest.mark.benchmark(group="multiply_vectors")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_vectors_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as vectors)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    vec_1 = vec_generator(sz)
    vec_2 = vec_generator(sz)

    benchmark(client.multiply, vec_1, vec_2)


@pytest.mark.benchmark(group="add_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_add_matrices_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the addition of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.add, mat_1, mat_2)


@pytest.mark.benchmark(group="multiply_matrices")
@pytest.mark.parametrize("sz", SIZES, ids=SIZES_IDS)
def test_multiply_matrices_rest_python(benchmark, sz):
    """BM test to measure the time consumed so that the client gets the expected response
    when performing the multiplication of two numpy arrays (as matrices)."""
    client = DemoRESTClient("http://0.0.0.0", 5000)

    mat_1 = mat_generator(sz)
    mat_2 = mat_generator(sz)

    benchmark(client.multiply, mat_1, mat_2)
