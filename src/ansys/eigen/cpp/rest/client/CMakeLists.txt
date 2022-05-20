cmake_minimum_required(VERSION 3.4...3.18)
project(api_eigen_example_rest_client VERSION 1.0 DESCRIPTION "The API Eigen Example project REST client implemented in C++")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# Link to the restclient-cpp and jsoncpplib
link_libraries(-lrestclient-cpp -ljsoncpp)

# Add the headers and sources for it to work
set(headers 
    src/EigenClient.hpp
)

set(sources 
    src/EigenClient.cpp
)

# Add the example executable
add_executable(cpp_rest_client src/main.cpp)
target_sources(cpp_rest_client PRIVATE ${headers} ${sources})

# Add the library - as shared
add_library(api_eigen_example_rest_client SHARED
    ${sources}
)
set_target_properties(api_eigen_example_rest_client PROPERTIES 
    PUBLIC_HEADER src/EigenClient.hpp
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
)
include(GNUInstallDirs)

install(TARGETS api_eigen_example_rest_client
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/apieigen/rest)