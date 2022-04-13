import time

from chunkdemo_pb2 import PopulateArrayRequest, StreamRequest
from chunkdemo_pb2_grpc import ChunkDemoStub
import grpc
import numpy as np

# chunk sizes for streaming and file streaming
DEFAULT_CHUNKSIZE = 256 * 1024  # 256 kB

# data mapping
C_TO_NP = {"INT32": np.int32}


class ChunkDemoClient:
    """ """

    def __init__(self, ip="127.0.0.1", port=50000, timeout=1):
        """Initialize connection to the mapdl server"""
        self._stub = None

        self._channel_str = "%s:%d" % (ip, port)

        # by default is limited to 4194304 bytes
        options = [("grpc.max_receive_message_length", 100 * 1024 * 1024)]
        self.channel = grpc.insecure_channel(self._channel_str, options=options)
        self._state = grpc.channel_ready_future(self.channel)
        self._stub = ChunkDemoStub(self.channel)

        # verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:
            raise IOError("Unable to connect to server at %s" % self._channel_str)

    def request_array(self, chunk_size=DEFAULT_CHUNKSIZE):
        """Request an array from the server"""
        request = StreamRequest()
        metadata = [("chunk_size", str(chunk_size))]
        chunks = self._stub.DownloadArray(request, metadata=metadata)
        return self._parse_chunks(chunks, np.int32)

    def request_array_from_repeated(self):
        request = StreamRequest()
        response = self._stub.DownloadArraySlow(request)
        # return np.array(response.ints)  # slow
        return np.fromiter(response.ints, dtype=np.int32)

    def populate_array(self, array_size):
        request = PopulateArrayRequest(array_size=array_size)
        return self._stub.PopulateArray(request)

    def _parse_chunks(self, chunks, dtype=None):
        """Deserialize chunks into a numpy array

        Parameters
        ----------
        chunks : generator
            generator from grpc.  Each chunk contains a bytes payload

        dtype : np.dtype
            Numpy data type to interpert chunks as.

        Returns
        -------
        array : np.ndarray
            Deserialized numpy array.

        """
        if not chunks.is_active():
            raise RuntimeError("Empty Record")

        # map chunk datatype to np.dtype
        metadata = dict(chunks.initial_metadata())
        dtype = C_TO_NP[metadata["datatype"]]
        size = int(metadata["size"])
        arr = np.empty(size, dtype=dtype)
        itemsize = np.dtype(np.int32).itemsize

        i = 0
        for chunk in chunks:
            arr[i : i + len(chunk.payload) // itemsize] = np.frombuffer(
                chunk.payload, dtype
            )
            i += len(chunk.payload) // itemsize

        return arr


if __name__ == "__main__":
    import timeit

    # connect to server
    ip = "127.0.0.1"
    port = 50000
    client = ChunkDemoClient(ip, port)
    print("Connected to server at %s:%d" % (ip, port))

    # Thanks SO
    # https://stackoverflow.com/a/1094933/3369879
    def sizeof_fmt(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, "Yi", suffix)

    # Start by initializing the array on the server
    array_size = 20000000
    client.populate_array(array_size)
    print("Created an INT32 array on the server size", array_size)

    ###########################################################################
    ### Download using chunks
    ###########################################################################
    print("Testing with byte stream...")
    n = 20
    out = timeit.timeit(
        "client.request_array()",
        setup="from __main__ import " + ", ".join(locals()),
        number=n,
    )
    tavg = out / n
    print("Average time:", tavg)
    arr_nbytes = client.request_array().nbytes
    bps = arr_nbytes / tavg

    print("Aprox speed:", sizeof_fmt(bps, suffix="B"))
    print()

    ###########################################################################
    ### Download using repeated messages
    ###########################################################################
    print("Testing with repeated messages...")
    client.populate_array(array_size)
    n = 3
    out = timeit.timeit(
        "client.request_array_from_repeated()",
        setup="from __main__ import " + ", ".join(locals()),
        number=n,
    )
    tavg = out / n
    print("Average time:", tavg)
    arr_nbytes = client.request_array_from_repeated().nbytes
    bps = arr_nbytes / tavg

    print("Aprox speed:", sizeof_fmt(bps, suffix="B"))
    print()
