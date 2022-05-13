#include <vector>

#include "EigenClient.hpp"

int main(int argc, char const *argv[]) {
    // ------------------------------------------------------------------------
    // Deploying the client
    // ------------------------------------------------------------------------
    // Instantiate an EigenClient
    auto client = ansys::rest::client::EigenClient("http://0.0.0.0:18080");

    // ------------------------------------------------------------------------
    // REQUESTING GREETING - A.K.A "Hello World"
    // ------------------------------------------------------------------------
    // Let us request a greeting!
    client.request_greeting();

    // ------------------------------------------------------------------------
    // Performing vector operations
    // ------------------------------------------------------------------------
    // Let us create some reference vectors
    std::vector<double> vec1{1.0, 2.0, 3.0, 50.0};
    std::vector<double> vec2{4.0, 5.0, 8.0, 10.0};

    // Let us add them
    client.add_vectors(vec1, vec2);

    // Let us ask for their dot product
    client.multiply_vectors(vec1, vec2);

    // ------------------------------------------------------------------------
    // Performing matrix operations
    // ------------------------------------------------------------------------
    // Let us create some reference matrices
    std::vector<std::vector<double>> mat1{{1.0, 2.0}, {3.0, 50.0}};
    std::vector<std::vector<double>> mat2{{4.0, 5.0}, {8.0, 10.0}};

    // Let us add them
    client.add_matrices(mat1, mat2);

    // Let us ask for their product
    client.multiply_matrices(mat1, mat2);

    // Exit successfully
    return 0;
}
