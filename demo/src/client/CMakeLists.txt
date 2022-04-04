add_executable(demo_client demo_client.cpp)
target_include_directories(demo_client PUBLIC ${CONAN_LIB_DIRS})
target_link_libraries(demo_client ${CONAN_LIBS})
target_link_libraries(demo_client send_array)
