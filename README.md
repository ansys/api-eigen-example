# API Eigen example project

## Introduction

The API Eigen example package is a simple project which intends to show PyAnsys
users and developers the differences existing between API REST communication protocol
and the well-known gRPC protocol, extensively used through the PyAnsys community.

The main goal of this demo is to expose the [Eigen library](https://eigen.tuxfamily.org/index.php?title=Main_Page)
to end users via a client-server interaction, which may be implemented using API REST or gRPC communication protocols.

The server will expose certain functionalities of the Eigen Library, such as adding and
multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` objects. The computational operations are
performed in the Eigen Library installed within the server and the results are returned to the
end-user (or client). Thus, it is not necessary for the client to have the Eigen Library installed,
for example.

The client is intended to aid the end-users since it provides them with the tools for
communicating with the server without needing to know the specifics of the protocol implemented.
However, feel free to interact directly by your own means with the server (e.g. API REST communication 
can also be easily performed using CURL commands).

## Getting Started
To use the API Eigen Example project you do not need any specific requirements or
additional software, apart from the ones to be installed via the requirements --all-files
and a CMake version of the Eigen library.

### Installation

First of all, it is necessary to install the Eigen library (and CMake if not present). For Ubuntu
distributions it is as easy as running the following:

```
    sudo apt install cmake libeigen3-dev
```

To install a local version of the API Eigen Example project, you need to clone the repository through
GitHub Enterprise (https://github.com/ansys/api-eigen-example).
Other Ansys Python packages are also available here or through www.pypi.org. 

```
    git clone https://github.com/ansys/api-eigen-example.git
```

In case we wanted to use the Python versions of the API Eigen Example project, it is necessary
that we first install the demo-eigen-wrapper (a wrapper to the Eigen library using pybind11).

```
    pip install -r requirements/requirements_eigen_wrapper.txt ./src/ansys/eigen/cpp/eigen-wrapper
```

And finally, you can install the project by doing as follows:

```
    pip install -r requirements/requirements_build.txt .
```

### Starting to use it

Once the API Eigen Example project has been installed, we can start to make use of the Python
packages by importing them as follows

```
    >>> import ansys.eigen.python.rest.server as rest_server
    >>> import ansys.eigen.python.rest.client as rest_client
    >>> client = rest_client.DemoRESTClient("127.0.0.1", 5000)
    >>> client.get_connection_details()
```

## Documentation

An automatically generated version of the project's documentation is published every night under the following [link](https://apieigen.docs.pyansys.com/).

Please, feel free to search on it more specific documentation of the project itself.

## IMPORTANT NOTE!!

This repository is **for demonstration purposes only**. It is not intended to expose the
Eigen Library as a service, nor is it expected to be used as a product. This demo is intended to be used for demonstrating
the REST and gRPC protocols via client-server interaction, with interactive examples, documentation and resources.

It provides a baseline (or guidelines) for future projects which may have to deal with API protocols such as REST and gRPC, in different languages,
with a higher level of complexity than a simple "Hello World" project.
