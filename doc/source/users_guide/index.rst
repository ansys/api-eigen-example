
.. _user_guide:

************
User's Guide
************
This guide contains pertinent information regarding the use of the API Eigen Example
demo package and its constituent modules and components.

=================================================
Understanding the API Eigen Example Python Module
=================================================
Within this project, the "ansys.eigen.python" package is the one which contains the necessary objects for
testing the different protocols (API REST, gRPC), implemented in Python. There are two other extra packages:

- The REST package: ``ansys.eigen.python.rest``
- The gRPC package: ``ansys.eigen.python.grpc``

Each of these two packages also contains two modules: ``client`` and ``server`` which are the key modules for
performing the demos. Let's look into each of the two packages (REST and gRPC)

----------------------------------------
The API REST Eigen Example Python Module
----------------------------------------

.. code:: python

   import ansys.eigen.python.rest.server as rest_server
   import ansys.eigen.python.rest.client as rest_client


The API REST Python server is characterized for being a Flask application, which
contains a SQLite DB. This server is intended to be run easily with the following
commands (in the terminal). If you were located at the root directory of the repository, and you wanted to
deploy the API REST version of the server, you could do the following:

.. code:: bash

   export FLASK_APP="src/ansys/eigen/python/rest/server.py"
   flask run

This will deploy the server by its default parameters, though you can always deploy it manually if you prefer by
calling the ``create_app()`` method, which returns the Flask App, and then running (i.e. ``app.run(...)``):

.. code:: python

   app = rest_server.create_app()
   app.run("127.0.0.1", 1234)

The Python client contains a class called ``DemoRESTClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if we wanted to create an API REST client for interacting with
our previously deployed server we would:

.. code:: python

   client = rest_client.DemoRESTClient("127.0.0.1", 1234)

This way, we would have our client available to perform operations such as the following:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   vec_add = client.add(vec_1, vec_2)             # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_sub = client.subtract(vec_1, vec_2)        # >>> numpy.ndarray([-4.0, -2.0,  1.0,  4.0])
   vec_mul = client.multiply(vec_1, vec_2)        # >>> 19 (== dot product of vec_1 and vec_2)

----------------------------------------
The API gRPC Eigen Example Python Module
----------------------------------------

.. code:: python

   import ansys.eigen.python.grpc.server as grpc_server
   import ansys.eigen.python.grpc.client as grpc_client


The API gRPC Python server is characterized for being a standalone grpc application, with no DB.
This server is intended to be run easily with the following commands (in the terminal). If you were located
at the root directory of the repository, and you wanted to deploy the API gRPC version of the server, you 
could do the following:

.. code:: bash

   python src/ansys/eigen/python/grpc/server.py

This will deploy the server by its default parameters, though you can always deploy it manually if you prefer by
calling the ``serve()`` method inside the module:

.. code:: python

   grpc_server.serve()

The Python client contains a class called ``DemoGRPCClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if we wanted to create an API gRPC client for interacting with
our previously deployed server we would:

.. code:: python

   cli = grpc_client.DemoGRPCClient(ip="127.0.0.1", port=50051)

This way, we would have our client available to perform operations such as the following:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   cli.request_greeting("James")                  # >>> Server answering  "Hello, James!"
   vec_add = cli.add_vectors(vec_1, vec_2)        # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_mul = cli.multiply_vectors(vec_1, vec_2)   # >>> 19 (== dot product of vec_1 and vec_2)