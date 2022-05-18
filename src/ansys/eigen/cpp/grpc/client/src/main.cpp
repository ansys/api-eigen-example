#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

#include "GRPCClient.hpp"

// ----------------------------------------------------------------------------
// AUXILIARY METHODS DECLARATION
// ----------------------------------------------------------------------------
void print_matrix(const std::string& name,
                  const std::vector<std::vector<double>>& mat);
void print_vector(const std::string& name, const std::vector<double>& vec);

int main() {
    // ------------------------------------------------------------------------
    // Deploying the client
    // ------------------------------------------------------------------------
    // Instantiate an GRPCClient
    ansys::grpc::client::GRPCClient client{"0.0.0.0", 50000};

    // ------------------------------------------------------------------------
    // REQUESTING GREETING - A.K.A "Hello World"
    // ------------------------------------------------------------------------
    // Let us request a greeting!
    client.request_greeting("Michael");

    // ------------------------------------------------------------------------
    // Performing vector operations
    // ------------------------------------------------------------------------
    // 1) Vector position flip
    std::vector<double> vec{1.0, 2.0, 3.0, 4.5, 6.7};
    print_vector("vec", vec);
    auto flip_vec = client.flip_vector(vec);
    print_vector("flip_vec", flip_vec);

    // 2) Vector addition
    std::vector<double> vec1{1.3, 2.7, 3.3, 4.5, 6.7};
    std::vector<double> vec2{7.1, 3.4, 2.3, 1.2, 8.1};
    print_vector("vec1", vec1);
    print_vector("vec1", vec2);
    auto add_vec = client.add_vectors(vec1, vec2);
    print_vector("add_vec", add_vec);

    // 2) Vector dot product
    auto mul_vec = client.multiply_vectors(vec1, vec2);
    print_vector("mul_vec", std::vector<double>{mul_vec});

    // ------------------------------------------------------------------------
    // Performing matrix operations
    // ------------------------------------------------------------------------

    // Exit successfully
    return 0;
}

// ----------------------------------------------------------------------------
// AUXILIARY METHODS IMPLEMENTATION
// ----------------------------------------------------------------------------

void print_matrix(const std::string& name,
                  const std::vector<std::vector<double>>& mat) {
    // Print out Matrix name
    std::cout << name << std::endl;
    int idx{0};
    for (const auto& vec : mat) {
        print_vector("row" + idx, vec);
        ++idx;
    }
}

void print_vector(const std::string& name, const std::vector<double>& vec) {
    // Define the ostring stream
    std::ostringstream vts;

    if (!vec.empty()) {
        // Convert all but the last element to avoid a trailing ","
        std::copy(vec.begin(), vec.end() - 1,
                  std::ostream_iterator<double>(vts, ", "));

        // Now add the last element with no delimiter
        vts << vec.back();
    }

    // Print out value
    std::cout << name << ": " << vts.str() << std::endl;
}
