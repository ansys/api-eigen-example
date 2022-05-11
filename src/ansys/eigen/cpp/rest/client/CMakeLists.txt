cmake_minimum_required(VERSION 3.4...3.18)
project(cpp_rest_client VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Link to the restclient-cpp and jsoncpplib
link_libraries(-lrestclient-cpp -ljsoncpp)

# Add the executable
add_executable(cpp_rest_client src/main.cpp)

# Add the headers and sources for it to work
set(headers 
    src/EigenClient.hpp
)

set(sources 
    src/EigenClient.cpp
)

target_sources(cpp_rest_client PRIVATE ${headers} ${sources})