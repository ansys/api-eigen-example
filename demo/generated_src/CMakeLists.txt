add_library(send_array STATIC chunkdemo.pb.cc chunkdemo.grpc.pb.cc)

target_include_directories(send_array PUBLIC ${CONAN_LIB_DIRS})
target_include_directories(send_array PUBLIC .)

target_link_libraries(send_array ${CONAN_LIBS})
