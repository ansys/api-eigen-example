add_executable(sync_server sync_server.cpp)
target_include_directories(sync_server PUBLIC ${CONAN_LIB_DIRS})

target_link_libraries(sync_server ${CONAN_LIBS})
target_link_libraries(sync_server send_array)
target_link_libraries(sync_server common)
