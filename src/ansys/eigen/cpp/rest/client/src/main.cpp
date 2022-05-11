#include <vector>

#include "EigenClient.hpp"

int main(int argc, char const *argv[]) {
    // Instantiate an EigenClient
    auto client = ansys::rest::client::EigenClient("http://0.0.0.0:18080");

    // Let us request a greeting!
    client.request_greeting();

    std::vector<double> vec1{1.0, 2.0, 3.0, 50.0};
    std::vector<double> vec2{4.0, 5.0, 8.0, 10.0};

    client.add_vectors(vec1, vec2);

    // Exit successfully
    return 0;
}
