#include "RestDb.hpp"
#include "RestServer.hpp"

int main() {
    // Let us instantiate our server
    ansys::rest::server::RestServer server{};

    // Start serving!
    server.serve();
}
