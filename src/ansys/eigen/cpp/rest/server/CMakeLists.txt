cmake_minimum_required(VERSION 3.4...3.18)
project(api_eigen_example_rest_server VERSION 1.0 DESCRIPTION "The API Eigen Example project REST server implemented in C++")

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# Call the CONAN setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Link to the CONAN_LIBS
link_libraries(${CONAN_LIBS})

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

# Add the example executable
add_executable(cpp_rest_server src/main.cpp)
target_sources(cpp_rest_server PRIVATE ${headers} ${sources})

# Add the library - as shared
add_library(api_eigen_example_rest_server SHARED
    ${sources}
)
set_target_properties(api_eigen_example_rest_server PROPERTIES 
    PUBLIC_HEADER src/RestServer.hpp
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
)
include(GNUInstallDirs)

install(TARGETS api_eigen_example_rest_server
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/apieigen/rest)