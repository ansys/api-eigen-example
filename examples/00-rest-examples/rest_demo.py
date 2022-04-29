"""
.. _ref_rest_demo_python:

API Eigen Example - REST Demo using Python
------------------------------------------

This tutorial shows how you can use the Python REST Client of the API Eigen Example
project to communicate with the REST Server.

In the following demo, we will be showing the basics of API REST protocols by means of a
simple library we have created. This library basically contains two elements in its Python version:

- A server which basically implements an API REST interface to communicate with an installed library within
    it, in our case the Eigen library. This API REST interface basically exposes certain functionalities such as
    adding, subtracting and multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` in a simple way.
- A client in charge of easing the interaction with the server by means of API REST interface specific methods.
    By using the client library, one does not need to know the specifics of the API REST interface.

In order to run this demo, it is necessary to deploy a server. When the docs are generated
(via workflows), the server is deployed as a service to compile the example. However, if you
are planning on running the example on your own, it is necessary to deploy it manually. In order to
do so, please run this on a different Python terminal:

>>> import ansys.eigen.python.rest.server as rest_server
>>> app = rest_server.create_app()
>>> app.run("127.0.0.1", 5000)

Now, once the server is up and running. Let us import our client!

"""

from ansys.eigen.python.rest.client import DemoRESTClient

###############################################################################
# The DemoRESTClient
# ~~~~~~~~~~~~~~~~~~
# This ``DemoRESTClient`` class is basically the one which will handle the API REST interface with
# the server, together with the connection itself, the formatting of the request and so on. When
# constructing the class we must provide as inputs the ``host`` and the ``port`` of the server. For this
# demo we are running, since we already deployed the server (either manually or as a service - i.e. container),
# we will provide us arguments:
#
# - Host: http://127.0.0.1
# - Port: 5000
#
# The server is exposed by **IP 127.0.0.1** and **port 5000** as per defined in the Dockerfile of the server
# (or if deployed manually, as specified previously). Thus, the previous inputs should be provided.
#
# This ``DemoRESTClient`` class also allows for Basic Authentication in case the server were to be protected.
# Please, see below how to provide the ``user`` and ``pwd`` in the following example:

my_client = DemoRESTClient("http://127.0.0.1", 5000)
my_client_ba = DemoRESTClient("http://127.0.0.1", 5000, user="myUser", pwd="myPwd")

###############################################################################
# This ``DemoRESTClient`` also has a method for retrieving the connection details of our client:

print("=========================")
my_client.get_connection_details()
print("=========================")
my_client_ba.get_connection_details()

###############################################################################
# Now, we will proceed to perform a simple operation like adding two 1D numpy.ndarrays. First, let us start by defining them:

import numpy as np

vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

###############################################################################
# Performing REST interaction
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Now, we will call the client method ``add(...)``, and we will explain the typical process of all interface methods (``add(...)``, ``subtract(...)`` and ``multiply(...)``):
#
# - The client performs some sanity checks to confirm that the inputs provided are as expected. This Demo has some limitations such as: only 1D, 2D numpy.ndarrays are allowed; they must be of type float64. However, if we were to interact directly with the server, much more considerations would have to be taken into account(regarding the format of the requests - that is the reason why we use a client library).
# - Once the client has checked that everything is fine to go, we POST our RESOURCES. Here is where the REST world starts:
#     - Servers expose resources, also known as entities, which are well understood if we compare them to objects. For example, if we want to POST a RESOURCE we should basically:
#         - ``POST`` to ``${server-uri}/${resource}`` --> In our demo: ``http://127.0.0.1:5000/Vectors``
#         - Our Demo server has two resources implemented ``Matrices`` and ``Vectors``. Hence, we can only handle 1D and 2D numpy.ndarrays.
#     - When POSTing a resource, the request body contains the resource's information (i.e. our request will contain the 1D numpy.ndarray we want to POST). This information is usually serialized into a JSON format and the expected keys must be known by the client and the server to allow a proper interfacing. In a real REST application, the server usually exposes its metadata, which is basically the schema/structure of the different entities implemented (their names, attributes etc). This way, end users know how to interact with the server without knowing the specifics of the implementation.
#         - Imagine we were to use CURL commands, the POST request for our first Vector would look something like this:
#         - ``curl -X POST "http://127.0.0.1:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[5, 23, 3, 4]}'``
#     - If the POST was successful, we will receive an HTTP Response which will contain in its body the ID of the posted resource.
#         - ``{"vector" : {"id" : 1235412 }}``
#     - The server contains a DB in which the resources posted are stored/retrieved.
# - After the POSTings are performed, we will now proceed to ask the server for a certain operation involving the resources submitted.
#     - Servers can also admit "operations". A typical standard for defining operation-endpoints would be:
#         - ``GET`` to ``${server-uri}/${operation}/${resource}`` --> In our demo: ``http://127.0.0.1:5000/add/Vectors``
#     - These GET requests will also contain in its body the IDs of the involved resources:
#         - Imagine we were to use CURL commands, the GET request for adding two Vectors would look something like this:
#         - ``curl -X GET "http://127.0.0.1:5000/add/Vectors" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'``
#     - The server will then interact with the DB, retrieve the Vectors, call the Eigen Library (via a dedicated wrapper using pybind11), perform the operation and return the result.
#     - The client will then receive a response containing the result of the operation:
#         - ``{"vector-addition" : {"result" : [2.0, 3.0, 5.0, 4.0] }}``
#         - The dedicated client implemented will then parse this JSON string and transform the resulting value into a numpy.ndarray.
#         - This way, the end user calls the client library with numpy.ndarrays and retrieves numpy.ndarrays, without having to know the specifics of the interface.
#
# Let us now call the method!
#

# Call the client to perform your desired operation
vec_add = my_client.add(vec_1, vec_2)

# Show the result!
print("Vector addition!")
print("================")
print(vec_add)

###############################################################################
# As mentioned before, there are several other methods implemented:

# Call the client to perform your desired operation
vec_sub = my_client.subtract(vec_1, vec_2)

# Show the result!
print("Vector subtraction!")
print("===================")
print(vec_sub)

###############################################################################

# Call the client to perform your desired operation
vec_mul = my_client.multiply(vec_1, vec_2)

# Show the result!
print("Vector dot product!")
print("===================")
print(vec_mul)

###############################################################################
# Let us show as well operations with 2D numpy.ndarrays (i.e. Matrices)

# Define your matrices
mat_1 = np.array([[1, 2], [3, 4]], dtype=np.float64)
mat_2 = np.array([[5, 4], [2, 0]], dtype=np.float64)

# Call the client to perform your desired operation
mat_add = my_client.add(mat_1, mat_2)

# Show the result!
print("Adding matrices!")
print("================")
print(mat_add)

###############################################################################

# Call the client to perform your desired operation
mat_sub = my_client.subtract(mat_1, mat_2)

# Show the result!
print("Subtracting matrices!")
print("=====================")
print(mat_sub)

###############################################################################

# Call the client to perform your desired operation
mat_mul = my_client.multiply(mat_1, mat_2)

# Show the result!
print("Multiplying matrices!")
print("=====================")
print(mat_mul)
