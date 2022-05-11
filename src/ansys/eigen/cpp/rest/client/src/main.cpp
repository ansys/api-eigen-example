#include "EigenClient.hpp"

int main(int argc, char const *argv[]) {
    // Instantiate an EigenClient
    auto client = ansys::rest::client::EigenClient("http://0.0.0.0:18080");

    // Let us request a greeting!
    client.request_greeting();

    // Exit successfully
    return 0;
}
