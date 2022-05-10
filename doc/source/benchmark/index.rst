.. _bm_results:

=================
Benchmark results
=================

One of the tasks of this project was to evaluate the performance of the different implementations (using REST/gRPC, impact of the language used etc.). In
order to do so, the following page was created in which the latest benchmark test results (uploaded to the repository) are shown.

We will categorize them according to their implementation language in the following sections. All sections have the following set of tests for both protocols:

* Adding two vectors of multiple sizes.
* Performing a dot product of two vectors of multiple sizes.
* Adding two square matrices of multiple sizes.
* Multiplying two matrices of multiple sizes.

The parametrized sizes for these benchmark tests are shown in the graphs, and are basically a sequence of powers of 2 (i.e. '2, 4, 8, 16...'). The final value
is currently set to 128, but it is easily adaptable.

Now, let us see the results!

**************************
Benchmark tests for Python
**************************

Let us explain the layout of the figures:

* All figures show results for both gRPC and REST benchmark tests.
* gRPC results are shown on the left-half side of the figure, whereas REST results are shown on the right-half side.
* In each of these two groups, tests are sorted from left to right depending on the size of the arrays used.

If we applied this to the first test shown, the order would be as follows (from left to right):

* gRPC "add_vectors" test with vectors of 2 elements.
* gRPC "add_vectors" test with vectors of 4 elements.
* gRPC "add_vectors" test with vectors of 8 elements.
* ...
* REST "add_vectors" test with vectors of 2 elements.
* REST "add_vectors" test with vectors of 4 elements.
* REST "add_vectors" test with vectors of 8 elements.
* ...

By analyzing the name format of the tests one can also identify its characteristics. For example

* **test_add_vectors_grpc[0128]** is telling us that we are running the "add_vectors" test, for the gRPC protocol with random vectors of size 128.
* **test_multiply_matrices_rest[0064]** is telling us that we are running the "multiply_matrices" test, for the REST protocol with random square matrices of size 64.

Adding vectors
~~~~~~~~~~~~~~

.. raw:: html
    :file: images/python/hist-add_vectors.svg

Multiplying vectors
~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/python/hist-multiply_vectors.svg

Adding matrices
~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/python/hist-add_matrices.svg

Multiplying matrices
~~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/python/hist-multiply_matrices.svg

***********************
Benchmark tests for C++
***********************

Coming soon!
