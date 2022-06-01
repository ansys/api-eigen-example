.. _bm_results:

=================
Benchmark results
=================

One of the tasks of this project was to evaluate the performance of the different implementations (using REST/gRPC, impact of the language used etc.). In
order to do so, the following page was created in which the latest benchmark test results (uploaded to the repository) are shown.

They are categorized according to their implementation language in the following sections. All sections have the following set of tests for both protocols:

* Adding two vectors of multiple sizes.
* Performing a dot product of two vectors of multiple sizes.
* Adding two square matrices of multiple sizes.
* Multiplying two matrices of multiple sizes.

The parametrized sizes for these benchmark tests are shown in the graphs, and are basically a sequence of powers of 2 (that is, '2, 4, 8, 16 etc.'). The final value
is currently set to 128, but it is easily adaptable.

*****************
Benchmark results
*****************

Benchmark results layout
~~~~~~~~~~~~~~~~~~~~~~~~

The layout of the figures is characterized as follows:

* All figures show results for benchmark tests parametrized as:
    * Language implementation: Python, C++
    * API Protocol: REST, gRPC
    * Number of elements in data structures (that is, size of vector, matrix)

Adding vectors
~~~~~~~~~~~~~~

.. raw:: html
    :file: images/add_vectors.svg

Multiplying vectors
~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/multiply_vectors.svg

Adding matrices
~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/add_matrices.svg

Multiplying matrices
~~~~~~~~~~~~~~~~~~~~

.. raw:: html
    :file: images/multiply_matrices.svg

