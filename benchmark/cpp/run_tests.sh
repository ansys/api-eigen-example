#!/bin/bash

# create a virtual environment and install requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
rm -rf .benchmarks

# clone api-eigen-example examples
rm -rf api-eigen-example
git clone --depth 1 https://github.com/ansys/api-eigen-example.git

# Install the C++ Client libraries 
# -------------------------------------------------------------------------
# 0) Enter the api-eigen-example repo
cd api-eigen-example

# 1) Installing the REST Client
sudo apt update && sudo apt install libcurl4-openssl-dev && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && sudo make install && cd -
sudo apt update && cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && sudo make install && cd - 
cd src/ansys/eigen/cpp/rest/client/build/ && cmake .. && cmake --build . && sudo make install && cd -

# 2) Installing the gRPC Client
cd src/ansys/eigen/cpp/grpc/client && make compile && sudo ./deploy_dependencies.sh && sudo make install && cd -

# 99) Exit the api-eigen-example repo
cd ..
# -------------------------------------------------------------------------

# Bind the C++ libraries
pip install bindings/cpp-clients

# Run the Docker containers for the servers
docker run -d -p 18080:18080 -it --name bm-cpp-rest-server ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest 
docker run -d -p 50000:50000 -it --name bm-cpp-grpc-server ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest

# Start running the benchmark tests
echo "Benchmarking api-eigen-example C++ packages"
pytest tests/ --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-warmup=true --benchmark-min-rounds=500

# Stop and remove the Docker containers for the servers
docker stop bm-cpp-rest-server bm-cpp-grpc-server && docker rm bm-cpp-rest-server bm-cpp-grpc-server

mkdir hist -p
rm hist/*
pytest-benchmark compare --histogram hist/hist --group-by group --sort fullname 1> /dev/null