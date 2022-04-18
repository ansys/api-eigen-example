import time

import grpc
from grpcdemo_pb2_grpc import GRPCDemoStub


class DemoGRPCClient:
    """The API Eigen Example client class for interacting via gRPC."""

    def __init__(self, ip="127.0.0.1", port=50000, timeout=1):
        """Initialize connection to the API Eigen server"""
        self._stub = None
        self._channel_str = "%s:%d" % (ip, port)

        self.channel = grpc.insecure_channel(self._channel_str)
        self._state = grpc.channel_ready_future(self.channel)
        self._stub = GRPCDemoStub(self.channel)

        # verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:
            raise IOError("Unable to connect to server at %s" % self._channel_str)
        else:
            print("Connected to server at %s:%d" % (ip, port))
