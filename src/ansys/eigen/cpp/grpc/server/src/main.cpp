#include "GRPCServer.hpp"

int main() {
    // Let us instantiate our server
    ansys::grpc::server::GRPCServer server;

    // And let us start serving!
    server.serve("0.0.0.0", 50000, false);

    return 0;
}
