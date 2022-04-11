API Eigen Example Documentation |version|
=========================================

.. toctree::
   :hidden:
   :maxdepth: 2

   getting_started/index
   users_guide/index
   api/index
   contributing

Introduction
------------
The API Eigen example package is a simple project which intends to show PyAnsys
users and developers the differences existing between API REST communication protocol
and the well-known gRPC protocol, extensively used through the PyAnsys community.

The main goal of this demo is to expose the `Eigen library <https://eigen.tuxfamily.org/index.php?title=Main_Page>`
to end users via a client-server interaction, which may be implemented using API REST or gRPC communication protocols.

The server will expose certain functionalities of the Eigen Library, such as adding and
multiplying ``Eigen::VectorXd`` and ``Eigen::MatrixXd`` objects. The computational operations are
performed in the Eigen Library installed within the server and the results are returned to the
end-user (or client). Thus, it is not necessary for the client to have the Eigen Library installed,
for example.

The client is intended to aid the end-users since it provides them with the tools for
communicating with the server without needing to know the specifics of the protocol implemented.
However, feel free to interact directly by your own means with the server (e.g. API REST communication 
can also be easily performed using CURL commands)

This demo project contains basically 4 different examples:
- A Python REST API demo using both client-server features, which has a wrapping over
  the Eigen library using pybind11.
- [IN PROGRESS] A C++ REST API demo using both client-server features, with direct interaction
  with the Eigen Library on the server side.
- [IN PROGRESS] A Python gRPC demo using both client-server features, which has a wrapping over
  the Eigen library using pybind11.
- [IN PROGRESS] A C++ gRPC demo using both client-server features, with direct interaction
  with the Eigen Library on the server side.

Features
--------
This demo package provides features such as:

- Client providing end-users the capability to perform server-side operations
  without knowing details on the communication protocol being employed.
- Core examples on how to expose a service (i.e. the Eigen Library) via a server using
  different communication protocols.
- Benchmark tests showing the performance of each of the client-server and programming
  language implementations.
- and more...

Project Index
-------------

* :ref:`genindex`
