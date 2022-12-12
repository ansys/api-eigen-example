cmake_minimum_required(VERSION 3.4...3.18)
project(api_eigen_example_grpc_client VERSION 1.0 DESCRIPTION "The API Eigen Example project gRPC client implemented in C++")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# Call the CONAN setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Link to the CONAN_LIBS
link_libraries(${CONAN_LIBS})

# Add the headers and sources for it to work
set(headers 
    src/GRPCClient.hpp
    src/generated/grpcdemo.pb.h
    src/generated/grpcdemo.grpc.pb.h
)

set(sources 
    src/GRPCClient.cpp
    src/generated/grpcdemo.pb.cc
    src/generated/grpcdemo.grpc.pb.cc
)
# Add the example executable
add_executable(cpp_grpc_client src/main.cpp)
target_sources(cpp_grpc_client PRIVATE ${headers} ${sources})

# Add the library - as shared
add_library(api_eigen_example_grpc_client SHARED
    ${sources}
)
set_target_properties(api_eigen_example_grpc_client PROPERTIES 
    PUBLIC_HEADER ${headers}
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
)
include(GNUInstallDirs)

install(TARGETS api_eigen_example_grpc_client
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/apieigen/grpc)

install(DIRECTORY src/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/apieigen/grpc FILES_MATCHING PATTERN "*.h")