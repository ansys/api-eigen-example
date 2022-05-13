.. _getting_started:

***************
Getting Started
***************

The API Eigen example package is a simple project which intends to show PyAnsys
users and developers the differences existing between API REST communication protocol
and the well-known gRPC protocol, extensively used through the PyAnsys community.

This project has multiple language implementations as we will see in this chapter.

================================
API Eigen Example Python Project
================================

To use the API Eigen Example project in its Python version you do not need any specific requirements or
additional software, apart from the ones to be installed via the requirements --all-files
and a CMake version of the Eigen library. 

------------
Installation
------------

First of all, it is necessary to install the Eigen library (and CMake if not present). For Ubuntu
distributions it is as easy as running the following:

.. code:: bash

    sudo apt install cmake libeigen3-dev

To install a local version of the API Eigen Example project, you need to clone the repository through
GitHub Enterprise (https://github.com/ansys/api-eigen-example).
Other Ansys Python packages are also available here or through https://www.pypi.org. 

.. code:: bash

	git clone https://github.com/ansys/api-eigen-example.git

In case we wanted to use the Python versions of the API Eigen Example project, it is necessary
that we first install the demo-eigen-wrapper (a wrapper to the Eigen library using pybind11).

.. code:: bash

    pip install -r requirements/requirements_eigen_wrapper.txt ./src/ansys/eigen/cpp/eigen-wrapper

And finally, you can install the project by doing as follows:

.. code:: bash

    pip install -r requirements/requirements_build.txt .

------------------
Starting to use it
------------------

Once the API Eigen Example project has been installed, we can start to make use of the Python
packages by importing them as follows

.. code:: python

    >>> import ansys.eigen.python.rest.server as rest_server
    >>> import ansys.eigen.python.rest.client as rest_client
    >>> client = rest_client.DemoRESTClient("127.0.0.1", 5000)
    >>> client.get_connection_details()

For more examples, please refer to the :ref:`user_guide`.


=============================
API Eigen Example C++ Project
=============================

------------
Installation
------------

To use the API Eigen Example C++ projects, the installation process is a bit more cumbersome.
First of all, you would need to install the following packaged libraries: cmake.

.. code:: bash

    sudo apt install cmake


Now depending on the C++ project, the dependencies may vary. Go into your sections of interest from the ones below!

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ REST Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ REST server manually is a very simple process. Just run the following command lines from
the root of the repository.

.. code:: bash

    pip install -r requirements/requirements_build.txt .
    cd src/ansys/eigen/cpp/rest/server/build/
    conan install .. && cmake .. && cmake --build . && sudo make install


You are ready to go with the C++ REST Server! Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

.. code:: cpp

    #include <apieigen/rest/RestServer.hpp>

    int main() {
       // Let us instantiate our server
       ansys::rest::server::RestServer server{};

       // Start serving!
       server.serve();
    }


For compiling, just link the library as follows:

.. code:: bash

    g++ -o myServer main.cpp -lapieigen_example_rest_server


And run your server!

.. code:: bash

    ./myServer


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installation of the C++ REST Client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the C++ REST client manually is a little bit more complex process. We will have to install some
development libraries and compile (in place) some additional external libraries.

First, we need to install a ``dev`` version of ``libcurl``. Using an Ubuntu package manager as ``apt``, one should have to do as follows:

.. code:: bash

    sudo apt install libcurl4-openssl-dev

Once we have ``libcurl-dev`` installed, we now have to compile some external projects. These external projects have been frozen at a given version
within this repository and they can be found in the ``external`` folder. To install them, just follow the next steps:

.. code:: bash

    sudo apt update && sudo apt install libcurl4-openssl-dev && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && sudo make install && cd -
    sudo apt update && cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && sudo make install && cd - 


Now, once we have all dependencies installed, we will build and install the client library!

.. code:: bash

    cd src/ansys/eigen/cpp/rest/client/build/ && cmake .. && cmake --build . && sudo make install && cd -


And that's it! You are ready to use the REST C++ Client library. Start writing your own C++ ``client.cpp`` file and
include the project header files as follows:

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

       // Exit successfully
       return 0;
   }


For compiling, just link the library as follows:

.. code:: bash

    g++ -o myClientApp client.cpp -lapieigen_example_rest_client


And run your client application!

.. code:: bash

    ./myClientApp



