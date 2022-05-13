# Using the Docker containers

## API REST using Python
For this case scenario, there are 2 Docker containers, which have to be built the following way:
* **python-rest-client**: Docker container with the needed packages for running the implemented client (i.e. ```from ansys.eigen.python.rest.client import DemoRESTClient```).
* **python-rest-server**: Docker container with the needed packages for running the server with the Eigen library solver.

In order to build them, run from the root directory of the repository the following command:
```
docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-client:latest -f docker/python-rest-client/Dockerfile .
docker image build -t ghcr.io/ansys/api-eigen-example/python-rest-server:latest -f docker/python-rest-server/Dockerfile .
```

Or you can just pull them from the GitHub Container Registry repository:
```
docker pull ghcr.io/ansys/api-eigen-example/python-rest-server:latest
docker pull ghcr.io/ansys/api-eigen-example/python-rest-client:latest
```

In case you wanted to access the Docker-compose demo, please do as follows:
```
cd docker/python-rest
docker-compose up -d && docker-compose logs

# You will see some information regarding the Jupyter Notebook server deployed, and the token
# required to access it. Something like...
#
# http://127.0.0.1:8888/?token=d4d38b9197aebd2adb6b69ded0f79346c5809eddc593e366
#
# Access it with your desired web-browser
firefox http://127.0.0.1:8888/?token=...
```

Feel free to play around with the ```demo.ipynb``` Jupyter Notebook =)


## API gRPC using Python
For this case scenario, there are 2 Docker containers, which have to be built the following way:
* **python-grpc-client**: Docker container with the needed packages for running the implemented client (i.e. ```from ansys.eigen.python.grpc.client import DemoGRPCClient```).
* **python-grpc-server**: Docker container with the needed packages for running the server with the Eigen library solver.

In order to build them, run from the root directory of the repository the following command:
```
docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-client:latest -f docker/python-grpc-client/Dockerfile .
docker image build -t ghcr.io/ansys/api-eigen-example/python-grpc-server:latest -f docker/python-grpc-server/Dockerfile .
```

Or you can just pull them from the GitHub Container Registry repository:
```
docker pull ghcr.io/ansys/api-eigen-example/python-grpc-server:latest
docker pull ghcr.io/ansys/api-eigen-example/python-grpc-client:latest
```
In case you wanted to access the Docker-compose demo, please do as follows:
```
cd docker/python-grpc
docker-compose up -d && docker-compose logs

# You will see some information regarding the Jupyter Notebook server deployed, and the token
# required to access it. Something like...
#
# http://127.0.0.1:8888/?token=d4d38b9197aebd2adb6b69ded0f79346c5809eddc593e366
#
# Access it with your desired web-browser
firefox http://127.0.0.1:8888/?token=...
```

Feel free to play around with the ```demo.ipynb``` Jupyter Notebook =)

## API REST using C++
For this case scenario, there are 2 Docker containers, which have to be built the following way:
* **cpp-rest-client**: Docker container with the needed packages for running the implemented client (i.e. ```#include <apieigen/rest/EigenClient.hpp>```).
* **cpp-rest-server**: Docker container with the needed packages for running the server with the Eigen library solver.

In order to build them, run from the root directory of the repository the following command:
```
docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest -f docker/cpp-rest-client/Dockerfile .
docker image build -t ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest -f docker/cpp-rest-server/Dockerfile .
```

Or you can just pull them from the GitHub Container Registry repository:
```
docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest
docker pull ghcr.io/ansys/api-eigen-example/cpp-rest-client:latest
```

In case you wanted to access the Docker-compose demo, please do as follows:
```
cd docker/cpp-rest
docker-compose up -d && docker-compose logs

# You will see some information regarding the Jupyter Notebook server deployed, and the token
# required to access it. Something like...
#
# http://127.0.0.1:8888/?token=d4d38b9197aebd2adb6b69ded0f79346c5809eddc593e366
#
# Access it with your desired web-browser
firefox http://127.0.0.1:8888/?token=...
```

Even though we are dealing with a C++ implementation, thanks to [cling](https://root.cern/cling/) and
[xeus-cling](https://github.com/jupyter-xeus/xeus-cling), we are capable of demonstrating
via Jupyter Notebooks the functionalities of the C++ client as if it were an interpretable language (like Python or Matlab). 
Special thanks to their contributors! Did a great job there.


Feel free to play around with the ```demo.ipynb``` Jupyter Notebook =)
