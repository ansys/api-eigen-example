cmake_minimum_required(VERSION 3.4...3.18)
project(eigen_cpp_client)

# Add the pybind11 library to the CMake project - after being installed as " pip install "pybind11[global]" "
find_package(pybind11 REQUIRED)
include_directories(${PYBIND11_INCLUDE_DIR})

# Link to the gRPC C++ client library
link_libraries(-lapi_eigen_example_grpc_client -lapi_eigen_example_rest_client)

# add_subdirectory(pybind11)
pybind11_add_module(eigen_cpp_client src/main.cpp)

# VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(eigen_cpp_client
                           PRIVATE VERSION_INFO=${VERSION_INFO})
