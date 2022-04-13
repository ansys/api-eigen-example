.. _getting_started:

===============
Getting Started
===============
To use the API Eigen Example project you do not need any specific requirements or
additional software, apart from the ones to be installed via the requirements --all-files
and a CMake version of the Eigen library.

************
Installation
************

First of all, it is necessary to install the Eigen library (and CMake if not present). For Ubuntu
distributions it is as easy as running the following:

.. code:: bash

    sudo apt install cmake libeigen3-dev

To install a local version of the API Eigen Example project, you need to clone the repository through
GitHub Enterprise (https://github.com/ansys/api-eigen-example).
Other Ansys Python packages are also available here or through www.pypi.org. 

.. code:: bash

	git clone https://github.com/pyansys/pyfluent.git

In case we wanted to use the Python versions of the API Eigen Example project, it is necessary
that we first install the demo-eigen-wrapper (a wrapper to the Eigen library using pybind11).

.. code:: bash

    pip install -r requirements/requirements_eigen_wrapper.txt ./python/eigen-wrapper

And finally, you can install the project by doing as follows:

.. code:: bash

    pip install -r requirements/requirements_build.txt .


******************
Starting to use it
******************

Once the API Eigen Example project has been installed, we can start to make use of the Python
packages by importing them as follows

.. code:: python

    >>> import python.rest.server as rest_server
    >>> import python.rest.client as rest_client
    >>> client = rest_client.DemoRESTClient("127.0.0.1", 5000)
    >>> client.get_connection_details()

For more examples, please refer to the User's guide.



