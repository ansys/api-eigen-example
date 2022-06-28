# API Eigen Example project

## IMPORTANT

This repository is **for demonstration purposes only**. It is not intended to expose the
Eigen library as a service, nor is it expected to be used as a product. This demo is for demonstrating
the REST and gRPC communication protocols via client-server interactions, with interactive examples,
documentation, and resources.

The repository provides a baseline (or guidelines) for future projects that have to deal with API protocols such as REST and gRPC, in different languages,
with a higher level of complexity than a simple "Hello World" project.


## Table of contents

<!--ts-->
   * [Introduction](#introduction)
   * [Documentation](#documentation)
   * [Getting Started with the Python Packages](#getting-started-with-the-python-packages)
      * [Installation](#installation)
      * [Starting to use it](#starting-to-use-it)
   * [Getting Started with the C++ Packages](#getting-started-with-the-c-packages)
      * [Installing the C++ REST Server](#installing-the-c-rest-server)
      * [Installing the C++ REST Client](#installing-the-c-rest-client)
      * [Installing the C++ gRPC Server](#installing-the-c-grpc-server)
      * [Installing the C++ gRPC Client](#installing-the-c-grpc-client)
<!--te-->

## Introduction

The API Eigen Example package is a simple packing for showing PyAnsys
users and developers the differences between the API REST communication protocol
and the gRPC communication protocol that is used extensively in PyAnsys libraries.

The main goal of this demo is to expose the [Eigen library](https://eigen.tuxfamily.org/index.php?title=Main_Page)
to end users via a client-server interaction that can be implemented using API REST
or gRPC communication protocols.

The server exposes certain functionalities of the Eigen library, such as adding and
multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` objects. The computational operations are
performed in the Eigen library installed within the server, and results are returned to the
end user (or client). Thus, it is not necessary for the client to have the Eigen library installed.

The client is intended to aid end users because it provides them with tools for
communicating with the server without needing to know the specifics of the protocol implemented.
However, you can use CURL commands to interact directly with the server via API REST communication.

## Documentation

An automatically generated version of the project's documentation is published every night at [link](https://apieigen.docs.ansys.com/).
You can search the documentation for more specific information on the project itself.

## Getting started with the Python packages

To use the API Eigen Example Python project in its Python version, you do not need any specific requirements or
additional software, apart from the ones that are installed via the requirements ``--all-files``
and a CMake version of the Eigen library.

### Installation

First install the Eigen library (and CMake if it is not present). For Ubuntu distributions, it is as easy as running:

```
    sudo apt install cmake libeigen3-dev
```

To install a local version of the API Eigen Example project, clone the `repository <https://github.com/ansys/api-eigen-example>`_ through
the Ansys GitHub Enterprise account:

```
    git clone https://github.com/ansys/api-eigen-example.git
```

**Note**: 
Other Ansys Python packages are available through the Ansys GitHub Enterprise account or
through `PyPI <https://www.pypi.org>`_. 

If you want to use Python versions of the API Eigen Example project, install the demo-eigen-wrapper, which is a wrapper to the Eigen library that uses pybind11:

```
    pip install -r requirements/requirements_eigen_wrapper.txt ./src/ansys/eigen/cpp/eigen-wrapper
```

Finally, install the project with:

```
    pip install -r requirements/requirements_build.txt .
```

### Starting to use it

Once the API Eigen Example project has been installed, start to make use of the Python
packages by importing them:

```
    >>> import ansys.eigen.python.rest.server as rest_server
    >>> import ansys.eigen.python.rest.client as rest_client
    >>> client = rest_client.DemoRESTClient("127.0.0.1", 5000)
    >>> client.get_connection_details()
```

## Getting Started with the C++ packages
To use the API Eigen Example C++ projects, the installation process is a bit more cumbersome.
First install the packaged library ``cmake``:

```bash
    sudo apt install cmake
```

Depending on the C++ project, dependencies vary. Go to your sections of interest from those that follow.

### Installing the C++ REST server

Installing the C++ REST server manually is a simple process. Run the following commands from
the root of the repository.

```bash
    pip install -r requirements/requirements_build.txt .
    cd src/ansys/eigen/cpp/rest/server/build/
    conan install .. && cmake .. && cmake --build . && sudo make install
```

Once dependencies are installed, you can use the C++ REST server. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

```cpp
    #include <apieigen/rest/RestServer.hpp>

    int main() {
       // Let us instantiate our server
       ansys::rest::server::RestServer server{};

       // Start serving!
       server.serve();
    }
```

For compiling, link the library with:

```bash
    g++ -o myServer main.cpp -lapi_eigen_example_rest_server
```

You can run your server with:

```bash
    ./myServer
```

### Installing the C++ REST client

Installing the C++ REST client manually is a bit more complex. You must install some
development libraries and compile in place some additional external libraries.

First, install a ``dev`` version of ``libcurl``. Using the Ubuntu package manager ``apt``, you can run:

```bash
    sudo apt install libcurl4-openssl-dev
```

Once  ``libcurl-dev`` is installed, you must compile some external projects. These external projects have been frozen at a given version
within this repository. You can find them in the ``external`` folder. To install them, run these commands:

```bash
    sudo apt update && sudo apt install libcurl4-openssl-dev && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && sudo make install && cd -
    sudo apt update && cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && sudo make install && cd - 
```

Once dependencies are installed, you can build and install the client library with:

```bash
    cd src/ansys/eigen/cpp/rest/client/build/ && cmake .. && cmake --build . && sudo make install && cd -
```

You can now use the REST C++ client library. Start writing your own C++ ``client.cpp`` file and
include the project header files as follows:

```cpp

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
```

For compiling, link the library as follows:

```bash
    g++ -o myClientApp client.cpp -lapi_eigen_example_rest_client
```

You can run your client app with:

```bash
    ./myClientApp
```

### Installing the C++ gRPC Server

Installing the C++ gRPC server manually is a simple process. To use the [conan](https://conan.io/) package manager
to install dependencies, run the following command lines from the root of the repository:

```bash
    cd src/ansys/eigen/cpp/grpc/server/
    make compile && make install && ./deploy_dependencies.sh
```

You might need to run the previous ``install`` and ``deploy`` commands with root privileges.

Once dependencies are installed, you can use the C++ gRPC server. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

```cpp
    #include <apieigen/grpc/GRPCServer.hpp>

    int main() {
       // Let us instantiate our server
       ansys::grpc::server::GRPCServer server{};

       // Start serving!
       server.serve();
    }
```

For compiling, link the library as follows:

```bash
    g++ -o myServer main.cpp -lapi_eigen_example_grpc_server
```

You can run your server with:

```bash
    ./myServer
```

### Installing the C++ gRPC Client

Installing the C++ gRPC client manually is a simple process. To use the [conan](https://conan.io/) package manager
to install its dependencies, run the following commands from the root of the repository:

```bash
    cd src/ansys/eigen/cpp/grpc/client/
    make compile && make install && ./deploy_dependencies.sh
```

You might need to run the previous ``install`` and ``deploy`` commands with root privileges.

Once dependencies are installed, you can use the C++ gRPC client. Start writing your own C++ ``main.cpp`` file and
include the project header files as follows:

```cpp
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
```

For compiling, link the library as follows:

```bash
    g++ -o myClientApp main.cpp -lapi_eigen_example_grpc_client
```

You can run your client with:

```bash
    ./myClientApp
```
