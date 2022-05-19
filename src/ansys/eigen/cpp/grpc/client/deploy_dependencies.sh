#!/bin/bash

for value in grpc c-ares abseil openssl zlib re2 protobuf
do
    \cp -r build/$value/include/* /usr/local/include/
    \cp -r build/$value/lib/* /usr/local/lib/
    \cp -r build/$value/bin/* /usr/local/bin/
done