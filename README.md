### Large Array Serialization using gRPC

#### Prerequisites

Install `gRPC` for C++ using by following the directions at [gRPC Quick Start](https://grpc.io/docs/languages/cpp/quickstart/).  This will install both `gRPC` and `protobuf`, which you will need to compile the server and client.  If you wish you use the Python server as well, install `Python 3.6` or newer.

You will also need `cmake` to build the server and client, and the directions for installing a modern version of `cmake` are also at [gRPC Quick Start](https://grpc.io/docs/languages/cpp/quickstart/).


#### C++ Server

Enter the `cpp` directory and run the following to build the `demo_server`

```
mkdir build
cd build
cmake ..
make -j
```

Next, start the `demo_server` with:


```
./demo_server
```

You should see:

```
Server listening on 0.0.0.0:50000
```

The C++ server is now waiting for connections from port 50000.


#### C++ Client

After compiling the C++ server, start the C++ client with

```
./demo_client
```

This will automatically run the streaming demo:

```
./demo_client
Connected to server at: localhost:50000
Created an INT32 array on the server size 10000000
Array is 38.15 MB

Testing with byte stream...
Using chunk size 256 kB
Average time: 0.0167268
Approx speed: 2.23 GBps

Testing with repeated messages...
Average time: 0.0932537
Approx speed: 409.07 MBps

Testing with repeated chunked messages...
Average time: 0.0300367
Approx speed: 1.24 GBps

```

Use the `-h` flag to see the options available when running the client.

```
./demo_client -h
```

```
demo_client [options]
Options:
-h               Print this help
--target         Set the target channel (default localhost:50000)
--chunk_size     Set the chunk size in kB (default 256)
--skip_repeated  Skip testing the repeated messages
--array_size     Size of array in int32
--ntimes_stream  Number of times to test the stream
```

#### Python Client

First, ensure you have the following packages installed:

- `grpcio`
- `google-api-python-client`


Also, make sure that the version of the packages is greater than or equal to your `gRPC` C++ version.


Next, enter the `python` directory and run:

```
make
```

This will generate the python gRPC interface files `chunkdemo_pb2.py`
and `chunkdemo_pb2_grpc.py`.  While you have the C++ server running,
run:

```
python client.py
```

This will connect to the server at your local host and run a basic
array transfer test using both a byte stream and repeated messages.

```
Connected to server at 127.0.0.1:50000
Created an INT32 array on the server size 20000000
Testing with byte stream...
Average time: 0.03763810700038448
Aprox speed: 2.0GiB

Testing with repeated messages...
Average time: 0.8858063033355089
Aprox speed: 86.1MiB

```
