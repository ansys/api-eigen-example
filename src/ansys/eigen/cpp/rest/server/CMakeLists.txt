cmake_minimum_required(VERSION 3.4...3.18)
project(cpp_rest_server VERSION 1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the Crow, Boost and Eigen library to the CMake project - after being installed
find_package(Crow REQUIRED)
include_directories(${CROW_INCLUDE_DIR})

find_package(Boost 1.71.0 REQUIRED)
include_directories(${BOOST_INCLUDE_DIR})

find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})

# Link as well to the pthread lib and the sqlite3 lib
link_libraries(${Boost_LIBRARIES} pthread sqlite3)

# Add the source directories
include_directories(${BOOST_INCLUDE_DIR})

# Add the executable
add_executable(cpp_rest_server src/main.cpp)

# Add the DB sources for it to work
target_sources(cpp_rest_server PRIVATE src/RestDb.hpp src/RestDb.cpp src/RestServer.hpp src/RestServer.cpp src/EigenFunctionalities.hpp src/EigenFunctionalities.cpp)