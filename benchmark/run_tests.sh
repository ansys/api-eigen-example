#!/bin/bash

# create a virtual environment and install requirements
# -------------------------------------------------------------------------
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
# -------------------------------------------------------------------------
rm -rf .benchmarks

# clone api-eigen-example examples
# -------------------------------------------------------------------------
rm -rf api-eigen-example
git clone --depth 1 https://github.com/ansys/api-eigen-example.git

# Install the C++ Client libraries and other wrappers
# ========================================================================
# 0) Enter the api-eigen-example repo
cd api-eigen-example

# 1) Installing the REST Client
sudo apt update && sudo apt install libcurl4-openssl-dev && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && sudo make install && cd -
sudo apt update && cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && sudo make install && cd - 
cd src/ansys/eigen/cpp/rest/client/build/ && cmake .. && cmake --build . && sudo make install && cd -

# 2) Installing the gRPC Client
cd src/ansys/eigen/cpp/grpc/client && make compile && sudo ./deploy_dependencies.sh && sudo make install && cd -

# 3) Update the dynamic libraries
ldconfig -v

# 4) Install the eigen wrapper and requirements for api-eigen-example
pip install -r requirements/requirements_eigen_wrapper.txt
pip install src/ansys/eigen/cpp/eigen-wrapper
pip install -r requirements/requirements_build.txt

# 99) Exit the api-eigen-example repo
cd ..
# ========================================================================

# Run the Docker containers for the servers
# -------------------------------------------------------------------------
docker run -d -p  5000:5000  -it --name bm-python-rest-server ghcr.io/ansys/api-eigen-example/python-rest-server:latest
docker run -d -p 50051:50051 -it --name bm-python-grpc-server ghcr.io/ansys/api-eigen-example/python-grpc-server:latest
docker run -d -p 18080:18080 -it --name bm-cpp-rest-server    ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest 
docker run -d -p 50000:50000 -it --name bm-cpp-grpc-server    ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest

# Clean the tmp results folder  
# -------------------------------------------------------------------------
mkdir hist -p
rm hist/*

# Python BM tests
# -------------------------------------------------------------------------
# Start running the benchmarks
echo "Benchmarking api-eigen-example Python packages"
pip install api-eigen-example/
pytest tests/python/ --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-warmup=true --benchmark-min-rounds=500
pytest-benchmark compare --group-by group --sort fullname --csv=data/python_bm_results.csv 1> /dev/null

# C++ BM tests
# -------------------------------------------------------------------------
#
#
#
#
#

# Plot the results
# -------------------------------------------------------------------------
#
# Results should go to hist folder
#
#


# Stop and remove the Docker containers for the servers
# -------------------------------------------------------------------------
docker stop bm-python-rest-server bm-python-grpc-server bm-cpp-rest-server bm-cpp-grpc-server
docker rm   bm-python-rest-server bm-python-grpc-server bm-cpp-rest-server bm-cpp-grpc-server
