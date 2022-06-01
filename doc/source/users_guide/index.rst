
.. _user_guide:

************
User's guide
************
This guide contains pertinent information regarding the use of the API Eigen Example
demo package and its constituent modules and components.

=================================================
Understanding the API Eigen Example Python module
=================================================
Within this project, the "ansys.eigen.python" package is the one which contains the necessary objects for
testing the different protocols (API REST, gRPC), implemented in Python. There are two other extra packages:

- The REST package: ``ansys.eigen.python.rest``
- The gRPC package: ``ansys.eigen.python.grpc``

Each of these two packages also contains two modules: ``client`` and ``server`` which are the key modules for
performing the demos. This section is subdivided into each of the two packages (REST and gRPC).

----------------------------------------
The API REST Eigen Example Python module
----------------------------------------

.. code:: python

   import ansys.eigen.python.rest.server as rest_server
   import ansys.eigen.python.rest.client as rest_client


The API REST Python server is characterized for being a Flask app, which
contains a SQLite DB. This server is intended to be run easily with the following
commands (in the terminal). If you were located at the root directory of the repository, and you wanted to
deploy the API REST version of the server, you could do the following:

.. code:: bash

   export FLASK_APP="src/ansys/eigen/python/rest/server.py"
   flask run

This deploys the server by its default parameters, though you can always deploy it manually if you prefer by
calling the ``create_app()`` method, which returns the Flask App, and then running (that is, ``app.run(...)``):

.. code:: python

   app = rest_server.create_app()
   app.run("127.0.0.1", 1234)

The Python client contains a class called ``DemoRESTClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if the creation of an API REST client for interacting with
the previously deployed server is wanted, then:

.. code:: python

   client = rest_client.DemoRESTClient("127.0.0.1", 1234)

This way, the client is made available to perform operations such as the following:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   vec_add = client.add(vec_1, vec_2)             # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_sub = client.subtract(vec_1, vec_2)        # >>> numpy.ndarray([-4.0, -2.0,  1.0,  4.0])
   vec_mul = client.multiply(vec_1, vec_2)        # >>> 19 (== dot product of vec_1 and vec_2)

----------------------------------------
The API gRPC Eigen Example Python module
----------------------------------------

.. code:: python

   import ansys.eigen.python.grpc.server as grpc_server
   import ansys.eigen.python.grpc.client as grpc_client


The API gRPC Python server is characterized for being a standalone gRPC app, with no DB.
This server is intended to be run easily with the following commands (in the terminal). If you were located
at the root directory of the repository, and you wanted to deploy the API gRPC version of the server, you 
could do the following:

.. code:: bash

   python src/ansys/eigen/python/grpc/server.py

This deploys the server by its default parameters, though you can always deploy it manually if you prefer by
calling the ``serve()`` method inside the module:

.. code:: python

   grpc_server.serve()

The Python client contains a class called ``DemoGRPCClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if the creation of an API gRPC client for interacting with
the previously deployed server is wanted, then:

.. code:: python

   cli = grpc_client.DemoGRPCClient(ip="127.0.0.1", port=50051)

This way, the client is made available to perform operations such as the following:

.. code:: python

   vec_1 = np.array([1, 2, 3, 4], dtype=np.float64)
   vec_2 = np.array([5, 4, 2, 0], dtype=np.float64)

   cli.request_greeting("James")                  # >>> Server answering  "Hello, James!"
   vec_add = cli.add_vectors(vec_1, vec_2)        # >>> numpy.ndarray([ 6.0,  6.0,  5.0,  4.0])
   vec_mul = cli.multiply_vectors(vec_1, vec_2)   # >>> 19 (== dot product of vec_1 and vec_2)

==============================================
Understanding the API Eigen Example C++ module
==============================================

Within this project, apart from Python packages, there are also C++ projects. These projects are basically the C++ implementations
of the previously explained Python packages. They can be found within the repository in the following directories:

- The C++ REST projects: ``src/ansys/eigen/cpp/rest``
- The C++ gRPC projects: ``src/ansys/eigen/cpp/grpc``

Each of these two directories also contains two projects: ``client`` and ``server`` which are the key modules for
performing the demos. This section is subdivided into each of the two sets of projects (REST and gRPC).

---------------------------------------
The API REST Eigen Example C++ projects
---------------------------------------

First of all, you would need to install the projects. In order to do so, please follow the instructions in
:ref:`getting_started`

Assuming you have already installed them, start by doing some simple includes:

.. code:: cpp

   #include <apieigen/rest/EigenClient.hpp>
   #include <apieigen/rest/RestServer.hpp>


The API REST C++ server is characterized for being a CrowCpp app, which
contains a SQLite DB. This server is intended to be run easily with the following
commands. 

If you created a simple ``server.cpp`` file, you could do the following:

.. code:: cpp

   #include <apieigen/rest/RestServer.hpp>

   int main() {
      // Let us instantiate our server
      ansys::rest::server::RestServer server{};

      // Start serving!
      server.serve();
   }

If you know compiled the ``server.cpp`` file once the library is installed such that:

.. code:: bash

   g++ -o myServer server.cpp -lapi_eigen_example_rest_server

You would just have to run the outcoming executable from the compilation:

.. code:: bash
   
   ./myServer

And now, your server would be deployed.

.. code:: bash

   >>> Opened database successfully.
   >>> RestDb object created.
   >>> DB tables created successfully.
   >>> (2022-05-13 08:48:54) [INFO    ] REST Server object instantiated.
   >>> (2022-05-13 08:48:54) [INFO    ] Crow/1.0 server is running at http://0.0.0.0:18080 using 16 threads
   >>> (2022-05-13 08:48:54) [INFO    ] Call `app.loglevel(crow::LogLevel::Warning)` to hide Info level logs.

This deploys the server by its default parameters, though you can always deploy it with your own custom
parameters, by providing the optional inputs in the ``serve(...)`` method.

The C++ client contains a class called ``EigenClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if the creation of an API REST client for interacting with
the previously deployed server is wanted, write the following code snippet in a new C++ file to be called,
for example, ``client.cpp``:

.. code:: cpp

   #include <vector>

   #include <apieigen/rest/EigenClient.hpp>

   int main(int argc, char const *argv[]) {
       // ------------------------------------------------------------------------
       // Deploying the client
       // ------------------------------------------------------------------------
       // Instantiate an EigenClient
       auto client = ansys::rest::client::EigenClient("http://0.0.0.0:18080");

       // ------------------------------------------------------------------------
       // REQUESTING GREETING - A.K.A "Hello World"
       // ------------------------------------------------------------------------
       // Let us request a greeting!
       client.request_greeting();

       // ------------------------------------------------------------------------
       // Performing vector operations
       // ------------------------------------------------------------------------
       // Let us create some reference vectors
       std::vector<double> vec1{1.0, 2.0, 3.0, 50.0};
       std::vector<double> vec2{4.0, 5.0, 8.0, 10.0};

       // Let us add them
       auto result = client.add_vectors(vec1, vec2);

       // Exit successfully
       return 0;
   }


The previous client, for example, would deal with a vector addition operation via REST API interaction
with the server, apart from requesting a greeting.

In order to compile the client, one should do as follows:

.. code:: bash

   g++ -o myClientApp client.cpp -lapi_eigen_example_rest_client

And then you would just have to run the outcoming executable from the compilation:

.. code:: bash
   
   ./myClientApp

Enjoy creating your own apps.

---------------------------------------
The API gRPC Eigen Example C++ projects
---------------------------------------

First of all, you would need to install the projects. In order to do so, please follow the instructions in
:ref:`getting_started`

Assuming you have already installed them, start by doing some simple includes:

.. code:: cpp

   #include <apieigen/grpc/GRPCClient.hpp>
   #include <apieigen/grpc/GRPCServer.hpp>


The API gRPC C++ server is characterized for being a standalone gRPC app. This server is intended
to be run easily with the following commands. 

If you created a simple ``server.cpp`` file, you could do the following:

.. code:: cpp

   #include <apieigen/grpc/GRPCServer.hpp>

   int main() {
      // Let us instantiate our server
      ansys::grpc::server::GRPCServer server{};

      // Start serving!
      server.serve();
   }

If you know compiled the ``server.cpp`` file once the library is installed such that:

.. code:: bash

   g++ -o myServer server.cpp -lapi_eigen_example_grpc_server

You would just have to run the outcoming executable from the compilation:

.. code:: bash
   
   ./myServer

And now, your server would be deployed.

.. code:: bash

   >>> Instantiating our server...
   >>> GRPCService object created.
   >>> Server listening on 0.0.0.0:50000

This deploys the server by its default parameters, though you can always deploy it with your own custom
parameters, by providing the optional inputs in the ``serve(...)`` method.

The C++ client contains a class called ``GRPCClient``, which basically provide the end-user the tools to interact
directly with the previously deployed server. For example, if the creation of an API gRPC client for interacting with
the previously deployed server is wanted, write the following code snippet in a new C++ file to be called,
for example, ``client.cpp``:

.. code:: cpp

   #include <vector>

   #include <apieigen/grpc/GRPCClient.hpp>

   int main() {
       // ------------------------------------------------------------------------
       // Deploying the client
       // ------------------------------------------------------------------------
       // Instantiate a GRPCClient
       ansys::grpc::client::GRPCClient client{"0.0.0.0", 50000};

       // ------------------------------------------------------------------------
       // REQUESTING GREETING - A.K.A "Hello World"
       // ------------------------------------------------------------------------
       // Let us request a greeting!
       client.request_greeting("Michael");

       // ------------------------------------------------------------------------
       // Performing vector operations
       // ------------------------------------------------------------------------
       // Let us create some reference vectors
       std::vector<double> vec1{1.0, 2.0, 3.0, 50.0};
       std::vector<double> vec2{4.0, 5.0, 8.0, 10.0};

       // Let us add them
       auto result = client.add_vectors(vec1, vec2);

       // Exit successfully
       return 0;
   }


The previous client, for example, would deal with a vector addition operation via gRPC API interaction
with the server, apart from requesting a greeting.

In order to compile the client app, one should do as follows:

.. code:: bash

   g++ -o myClientApp client.cpp -lapi_eigen_example_grpc_client

And then you would just have to run the outcoming executable from the compilation:

.. code:: bash
   
   ./myClientApp

.. code:: bash

   GRPCClient object created.
   >>>> Requesting greeting for Michael
   >>>> Server answered --> Hello, Michael!
   >>>> Requesting vector addition!
   >>>> Server vector addition successful! Retrieving vector.
   GRPCClient object destroyed.

And on the server side you would be seeing these logs:

.. code:: bash

   >>>> Greeting requested! Requested by Michael
   >>>> Vector addition requested!
   >>>> Incoming Vector:  1  2  3 50
   >>>> Incoming Vector:  4  5  8 10
   >>>> Result of addition:  5  7 11 60
   Enjoy creating your own apps!

Enjoy creating your own apps.