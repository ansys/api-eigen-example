cmake_minimum_required(VERSION 3.4...3.18)
project(demo_eigen_wrapper)

# Add the Eigen library to the CMake project
find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})

add_subdirectory(pybind11)
pybind11_add_module(demo_eigen_wrapper src/main.cpp)

# VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(demo_eigen_wrapper
                           PRIVATE VERSION_INFO=${VERSION_INFO})
