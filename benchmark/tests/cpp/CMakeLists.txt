cmake_minimum_required(VERSION 3.4...3.18)
project(bm_api_eigen_example_tests VERSION 1.0 DESCRIPTION "The API Eigen Example project BM tests for C++")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# Link to the client libraries
link_libraries(-lapi_eigen_example_grpc_client -lapi_eigen_example_rest_client)

# Add the test executables
add_executable(add_matrices_grpc src/add_matrices_grpc.cpp)
add_executable(add_matrices_rest src/add_matrices_rest.cpp)

add_executable(add_vectors_grpc src/add_vectors_grpc.cpp)
add_executable(add_vectors_rest src/add_vectors_rest.cpp)

add_executable(multiply_matrices_grpc src/multiply_matrices_grpc.cpp)
add_executable(multiply_matrices_rest src/multiply_matrices_rest.cpp)

add_executable(multiply_vectors_grpc src/multiply_vectors_grpc.cpp)
add_executable(multiply_vectors_rest src/multiply_vectors_rest.cpp)