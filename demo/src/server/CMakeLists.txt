add_executable(demo_server demo_server.cpp)
target_include_directories(demo_server PUBLIC ${CONAN_LIB_DIRS})
target_link_libraries(demo_server ${CONAN_LIBS})
