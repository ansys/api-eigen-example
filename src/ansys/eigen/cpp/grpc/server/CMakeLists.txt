cmake_minimum_required(VERSION 3.4...3.18)
project(api_eigen_example_grpc_server VERSION 1.0 DESCRIPTION "The API Eigen Example project gRPC server implemented in C++")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Call the CONAN setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Link to the CONAN_LIBS
link_libraries(${CONAN_LIBS})

# Add the headers and sources for it to work
set(headers 
    src/GRPCServer.hpp
    src/generated/grpcdemo.pb.h
    src/generated/grpcdemo.grpc.pb.h
)

set(sources 
    src/GRPCServer.cpp
    src/generated/grpcdemo.pb.cc
    src/generated/grpcdemo.grpc.pb.cc
)

# Add the example executable
add_executable(cpp_grpc_server src/main.cpp)
target_sources(cpp_grpc_server PRIVATE ${headers} ${sources})

# Add the library - as shared
add_library(api_eigen_example_grpc_server SHARED
    ${sources}
)
set_target_properties(api_eigen_example_grpc_server PROPERTIES 
    PUBLIC_HEADER src/GRPCServer.hpp
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
)
include(GNUInstallDirs)

install(TARGETS api_eigen_example_grpc_server
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/apieigen/grpc)