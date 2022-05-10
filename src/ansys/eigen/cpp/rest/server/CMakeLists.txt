cmake_minimum_required(VERSION 3.4...3.18)
project(cpp_rest_server VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Call the CONAN setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Link to the CONAN_LIBS
link_libraries(${CONAN_LIBS})

# Add the executable
add_executable(cpp_rest_server src/main.cpp)

# Add the headers and sources for it to work
set(headers 
    src/RestDb.hpp
    src/RestServer.hpp
    src/EigenFunctionalities.hpp
)

set(sources 
    src/RestDb.cpp
    src/RestServer.cpp
    src/EigenFunctionalities.cpp
)

target_sources(cpp_rest_server PRIVATE ${headers} ${sources})