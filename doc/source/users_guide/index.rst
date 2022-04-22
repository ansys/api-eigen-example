
.. _user_guide:

************
User's Guide
************
This guide contains pertinent information regarding the use of the API Eigen Example
demo package and its constituent modules and components.

=================================================
Understanding the API Eigen Example Python Module
=================================================
Within this project, the "python" module is the one which contains the necessary objects for
testing the different protocols (API REST, gRPC), implemented in Python. For example, let's import
the server and the client submodules for the API REST protocol.

.. code:: python

   import ansys.eigen.python.rest.server as rest_server
   import ansys.eigen.python.rest.client as rest_client


The Python servers (for both API REST and gRPC) are characterized for being Flask applications, which
may contain a SQLite DB (at least for API REST). These servers are intended to be run easily with the following
commands (in the terminal). If you were located at the root directory of the repository, and you wanted to
deploy the API REST version of the server, you could do the following:

.. code:: bash

   export FLASK_APP="python/rest/server.py"
   flask run

This will deploy the server by its default parameters, though you can always deploy it manually if you prefer by
calling the ``create_app()`` method, which returns the Flask App, and then running it manually (i.e. ``app.run(...)``):

.. code:: python

   app = rest_server.create_app()
   app.run("127.0.0.1", 1234)

The Python clients contain classes called ``Demo****Client``, which basically provide the end-user the tools to interact
directly with the previously deployed servers. For example, if we wanted to create an API REST client for interacting with
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