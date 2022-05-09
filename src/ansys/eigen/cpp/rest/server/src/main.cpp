#include "RestDb.hpp"
#include "RestServer.hpp"

int main() {
    // Let us instantiate our server
    ansys::rest::RestServer server{};

    // Start serving!
    server.serve();
}
