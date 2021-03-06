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
sudo rm -rf api-eigen-example
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

# Clean the tmp results folder  
# -------------------------------------------------------------------------
rm -rf data/*.svg data/*.txt data/*.csv

# Python BM tests
# ========================================================================
# 
# Run the Docker containers for the servers
# -------------------------------------------------------------------------
docker run -d -p  5000:5000  -it --name bm-python-rest-server ghcr.io/ansys/api-eigen-example/python-rest-server:latest
docker run -d -p 50051:50051 -it --name bm-python-grpc-server ghcr.io/ansys/api-eigen-example/python-grpc-server:latest

# Start running the benchmarks
echo "Benchmarking api-eigen-example Python packages"
pip install api-eigen-example/

# Decompose the tests run to ease the execution
pytest tests/python/ -k 'grpc_python' --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-min-rounds=100
pytest tests/python/test_rest_python.py -k 'vectors_rest_python' --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-min-rounds=100
pytest tests/python/test_rest_python.py -k 'add_matrices_rest_python' --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-min-rounds=50
pytest tests/python/test_rest_python.py -k 'multiply_matrices_rest_python' --benchmark-save=main --benchmark-quiet --disable-warnings --no-header --benchmark-min-rounds=50
pytest-benchmark compare --group-by group --sort fullname --csv=data/python_bm_results.csv 1> /dev/null

# Stop and remove the Docker containers for the servers
# -------------------------------------------------------------------------
docker stop bm-python-grpc-server bm-python-rest-server && docker rm bm-python-grpc-server bm-python-rest-server

# C++ BM tests
# ========================================================================
# 
# Run the Docker containers for the servers
# -------------------------------------------------------------------------
docker run -d -p 18080:18080 -it --name bm-cpp-rest-server    ghcr.io/ansys/api-eigen-example/cpp-rest-server:latest 
docker run -d -p 50000:50000 -it --name bm-cpp-grpc-server    ghcr.io/ansys/api-eigen-example/cpp-grpc-server:latest

echo "Benchmarking api-eigen-example C++ packages"
cd tests/cpp/build
rm -rf *
cmake .. && cmake --build .
for test in add_vectors_rest add_vectors_grpc multiply_vectors_rest multiply_vectors_grpc add_matrices_rest add_matrices_grpc multiply_matrices_rest multiply_matrices_grpc
do
    echo "Running $test test..."
    ./$test &> /dev/null
    echo "Finished running $test test!"
    sleep 5
done
mv *].txt ../../../data/
cd -

# Stop and remove the Docker containers for the servers
# -------------------------------------------------------------------------
docker stop bm-cpp-rest-server bm-cpp-grpc-server
docker rm   bm-cpp-rest-server bm-cpp-grpc-server

# Plot the results
# -------------------------------------------------------------------------
cd data
python process_data.py
cd -
