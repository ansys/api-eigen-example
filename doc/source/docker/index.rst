.. _docker_examples:

===============
Docker examples
===============
As part of the development of this project, several Docker images have been created which allow
to use directly the client and server modules for both REST and gRPC using Python and C++. Depending
on the demo of interest to you, please refer to the corresponding section.

*********************
REST API using Python
*********************

For this specific demo, the following Docker containers are available:

- ``python-rest-client``: Docker container with the needed packages for running the implemented client (i.e. ``from ansys.eigen.python.rest.client import DemoRESTClient``).
- ``python-rest-server``: Docker container with the needed packages for running the server with the Eigen library solver.

These Docker containers are available at the GitHub Container Registry, so one can download the latest version by running:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/python-rest-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/python-rest-client:latest

However, you could also build them manually. In order to do so, please use the following commands from the root directory of the repository:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-server -f docker/python-rest-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-client -f docker/python-rest-client/Dockerfile .

The server Docker image is a standalone Flask app which starts up whenever the image is run. That way
the user does not have to perform any other operation apart from running the Docker image. To do this manually, one must run:

.. code:: bash

    docker run -d -p 5000:5000 -it ghcr.io/ansys/api-eigen-example/python-rest-server:latest

The client Docker image is a standalone JupyterLab app which starts up whenever the image is run. This JupyterLab
contains a demo Jupyter Notebook which one can run to test the client itself. Furthermore, one could open a new Jupyter
Notebook within the JupyterLab and start creating its own app. In order to run the client manually, one must:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/python-rest-client:latest

However, deploying the Docker containers manually is not the easiest way to test them. In order to start playing around with
them there is also available a docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/python-rest/docker-compose.yml

This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them,
since they are be located in the same Docker network. In order to launch the Docker compose task, simply run wherever the docker-compose.yml
file is located:

.. code:: bash

    docker-compose up -d

And start playing around with the Docker compose demo.

*********************
gRPC API using Python
*********************

For this specific demo, the following Docker containers are available:

- ``python-grpc-client``: Docker container with the needed packages for running the implemented client (i.e. from ``ansys.eigen.python.grpc.client import DemoGRPCClient``).
- ``python-grpc-server``: Docker container with the needed packages for running the server with the Eigen library solver.

These Docker containers are available at the GitHub Container Registry, so one can download the latest version by running:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/python-grpc-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/python-grpc-client:latest

However, you could also build them manually. In order to do so, please use the following commands from the root directory of the repository:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-server -f docker/python-grpc-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-client -f docker/python-grpc-client/Dockerfile .

The server Docker image is a standalone gRPC server which starts up whenever the image is run. That way
the user does not have to perform any other operation apart from running the Docker image. To do this manually, one must run:

.. code:: bash

    docker run -d -p 50051:50051 -it ghcr.io/ansys/api-eigen-example/python-grpc-server:latest

The client Docker image is a standalone JupyterLab app which starts up whenever the image is run. This JupyterLab
contains a demo Jupyter Notebook which one can run to test the client itself. Furthermore, one could open a new Jupyter
Notebook within the JupyterLab and start creating its own app. In order to run the client manually, one must:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/python-grpc-client:latest

However, deploying the Docker containers manually is not the easiest way to test them. In order to start playing around with
them there is also available a docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/python-grpc/docker-compose.yml

This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them,
since they are be located in the same Docker network. In order to launch the Docker compose task, simply run wherever the docker-compose.yml
file is located:

.. code:: bash

    docker-compose up -d

And start playing around with the Docker compose demo.

******************
REST API using C++
******************

For this specific demo, the following Docker containers are available:

- ``cpp-rest-client``: Docker container with the needed packages for running the implemented client (i.e. ``#include <apieigen/rest/EigenClient.hpp>``).
- ``cpp-rest-server``: Docker container with the needed packages for running the server with the Eigen library solver.

These Docker containers are available at the GitHub Container Registry, so one can download the latest version by running:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest

However, you could also build them manually. In order to do so, please use the following commands from the root directory of the repository:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-server -f docker/cpp-rest-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-client -f docker/cpp-rest-client/Dockerfile .

The server Docker image is a standalone `CrowCpp <https://crowcpp.org/>`_ app which starts up whenever the image is run. That way
the user does not have to perform any other operation apart from running the Docker image. To do this manually, one must run:

.. code:: bash

    docker run -d -p 18080:18080 -it ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest

The client Docker image is a standalone JupyterLab app which starts up whenever the image is run. This JupyterLab
contains a demo Jupyter Notebook which one can run to test the client itself. Furthermore, one could open a new Jupyter
Notebook within the JupyterLab and start creating its own app. In order to run the client manually, one must:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest

Even though dealing with a C++ implementation, thanks to `cling <https://root.cern/cling/>`_ and
`xeus-cling <https://github.com/jupyter-xeus/xeus-cling>`_, this demo is capable of demonstrating
via Jupyter Notebooks the functionalities of the C++ client as if it were an interpretable language (like Python or Matlab). 
Special thanks to their contributors. Did a great job there.

However, deploying the Docker containers manually is not the easiest way to test them. In order to start playing around with
them there is also available a docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/cpp-rest/docker-compose.yml

This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them,
since they are be located in the same Docker network. In order to launch the Docker compose task, simply run wherever the docker-compose.yml
file is located:

.. code:: bash

    docker-compose up -d

And start playing around with the Docker compose demo.

******************
gRPC API using C++
******************

For this specific demo, the following Docker containers are available:

- ``cpp-grpc-client``: Docker container with the needed packages for running the implemented client (i.e. ``#include <apieigen/grpc/GRPCClient.hpp>``).
- ``cpp-grpc-server``: Docker container with the needed packages for running the server with the Eigen library solver.

These Docker containers are available at the GitHub Container Registry, so one can download the latest version by running:

.. code:: bash

    docker pull ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest
    docker pull ghcr.io/ansys/api-eigen-example/cpp-grpc-client:latest

However, you could also build them manually. In order to do so, please use the following commands from the root directory of the repository:

.. code:: bash

    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-grpc-server -f docker/cpp-grpc-server/Dockerfile .
    docker image build -t ghcr.io/ansys/api-eigen-example/cpp-grpc-client -f docker/cpp-grpc-client/Dockerfile .

The server Docker image is a standalone gRPC app which starts up whenever the image is run. That way
the user does not have to perform any other operation apart from running the Docker image. To do this manually, one must run:

.. code:: bash

    docker run -d -p 50000:50000 -it ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest

The client Docker image is a standalone JupyterLab app which starts up whenever the image is run. This JupyterLab
contains a demo Jupyter Notebook which one can run to test the client itself. Furthermore, one could open a new Jupyter
Notebook within the JupyterLab and start creating its own app. In order to run the client manually, one must:

.. code:: bash

    docker run -d -p 8888:8888 -it ghcr.io/ansys/api-eigen-example/cpp-grpc-client:latest

Even though dealing with a C++ implementation, thanks to `cling <https://root.cern/cling/>`_ and
`xeus-cling <https://github.com/jupyter-xeus/xeus-cling>`_, this demo is capable of demonstrating
via Jupyter Notebooks the functionalities of the C++ client as if it were an interpretable language (like Python or Matlab). 
Special thanks to their contributors. Did a great job there.

However, deploying the Docker containers manually is not the easiest way to test them. In order to start playing around with
them there is also available a docker-compose task at https://github.com/ansys/api-eigen-example/blob/main/docker/cpp-grpc/docker-compose.yml

This task simplifies the deployment of both Docker containers and eases the configuration characteristics of each of them,
since they are located in the same Docker network. In order to launch the Docker compose task, simply run wherever the docker-compose.yml
file is located:

.. code:: bash

    docker-compose up -d

And start playing around with the Docker compose demo.